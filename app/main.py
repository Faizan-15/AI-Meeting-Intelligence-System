from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi import Depends
import os
import hashlib
import glob

from app.transcribe import convert_video_to_audio, transcribe_audio
from app.diarize import get_speaker_segments
from app.merge import merge_transcript_with_speakers
from app.database import init_db, get_db, Meeting
from app.services.llm_service import analyze_meeting
from app.services.qa_service import answer_question
from app.services.deadline_service import normalize_deadline
from app.schemas.meeting import MeetingAnalysis, ActionItem, MeetingQA
from app.cloud_storage import upload_file_bytes_to_s3, generate_presigned_url, delete_from_s3

app = FastAPI()

UPLOAD_DIR = "uploads"  # Keep for backward compatibility/fallback
VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv"]


@app.on_event("startup")
def on_startup():
    init_db()  # App start hote hi database tables ban jayengi


@app.get("/")
def home():
    return {"message": "Transcription Module is running"}


@app.post("/meeting/{meeting_id}/analyze")
def analyze_meeting_endpoint(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        return {"error": "Meeting not found"}
    if meeting.status != "completed":
        return {"status": "processing", "message": "Meeting still processing, analyze after completion"}

    transcript = meeting.full_text
    result = analyze_meeting(transcript)
    data = json.loads(result)

    return {"status": "completed", "analysis": data}


@app.post("/meeting/{meeting_id}/qa")
def meeting_qa_endpoint(
    meeting_id: int,
    question: str,
    db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        return {"error": "Meeting not found"}
    if meeting.status != "completed":
        return {"status": "processing", "message": "Meeting still processing, Q&A after completion"}

    transcript = meeting.full_text
    result = answer_question(transcript, question)
    return {"status": "completed", "question": question, "answer": result}


@app.post("/meeting/{meeting_id}/deadlines")
def extract_deadlines_endpoint(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        return {"error": "Meeting not found"}
    if meeting.status != "completed":
        return {"status": "processing", "message": "Meeting still processing, deadlines after completion"}

    transcript = meeting.full_text
    result = analyze_meeting(transcript)
    data = json.loads(result)

    # Extract deadlines from action items
    deadlines = []
    for item in data.get("action_items", []):
        deadline_normalized = normalize_deadline(item.get("deadline", ""), None)
        deadlines.append({
            "task": item.get("task"),
            "owner": item.get("owner"),
            "deadline": item.get("deadline"),
            "deadline_normalized": deadline_normalized,
            "timestamp": item.get("timestamp")
        })

    return {"status": "completed", "deadlines": deadlines}


def process_meeting(meeting_id: int, s3_key: str, filename: str):
    """Background mein chalne wala function - poora processing yahan hoti hai"""
    db = next(get_db())
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    try:
        UPLOAD_DIR = "uploads"
        VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv"]

        # Download from S3 to local temp path first
        import boto3
        from botocore.config import Config

        s3 = boto3.client(
            "s3",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            config=Config(signature_version="s3v4"),
        )
        bucket = os.getenv("AWS_S3_BUCKET")

        # Download file from S3
        local_file_path = os.path.join(UPLOAD_DIR, f"temp_{meeting_id}{os.path.splitext(filename)[1]}")
        s3.download_file(bucket, s3_key, local_file_path)

        ext = os.path.splitext(filename)[1].lower()

        if ext in VIDEO_EXTENSIONS:
            audio_path = os.path.join(UPLOAD_DIR, f"audio_{meeting_id}.wav")
            convert_video_to_audio(local_file_path, audio_path)
        else:
            audio_path = local_file_path

        transcript_result = transcribe_audio(audio_path)

        clean_whisper_segments = [
            {"start": seg["start"], "end": seg["end"], "text": seg["text"]}
            for seg in transcript_result["segments"]
        ]

        speaker_segments = get_speaker_segments(audio_path)
        final_transcript = merge_transcript_with_speakers(clean_whisper_segments, speaker_segments)

        duration = round(clean_whisper_segments[-1]["end"], 2) if clean_whisper_segments else 0

        # Database update karo - successful result
        meeting.status = "completed"
        meeting.duration_seconds = duration
        meeting.full_text = transcript_result["text"].strip()
        meeting.transcript_json = json.dumps(final_transcript)
        db.commit()

    except Exception as e:
        meeting.status = "failed"
        meeting.error_message = str(e)
        db.commit()

    finally:
        db.close()
        # Clean up local temp file
        import os
        temp_file = os.path.join(UPLOAD_DIR, f"temp_{meeting_id}*")
        for f in glob.glob(temp_file):
            try:
                os.remove(f)
            except:
                pass


@app.post("/upload-meeting")
async def upload_meeting(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    s3_key = f"uploads/{unique_filename}"

    # Read file bytes
    file_bytes = await file.read()
    
    # Upload to S3 instead of local storage
    if not upload_file_bytes_to_s3(file_bytes, s3_key, content_type=file.content_type or "application/octet-stream"):
        return {"error": "Failed to upload file to storage"}

    # Generate presigned URL for later access
    file_url = generate_presigned_url(s3_key)

    # Database mein ek naya record banao, status = "processing"
    new_meeting = Meeting(filename=file.filename, status="processing", filename_s3=s3_key)
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    # Processing background mein chalao (turant response wapas chala jayega)
    background_tasks.add_task(process_meeting, new_meeting.id, s3_key, file.filename)

    return {
        "message": "File uploaded to cloud, processing started",
        "meeting_id": new_meeting.id,
        "status": "processing",
        "file_url": file_url
    }


@app.get("/meeting/{meeting_id}/status")
def get_status(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        return {"error": "Meeting not found"}
    return {"meeting_id": meeting.id, "status": meeting.status}


@app.get("/meeting/{meeting_id}/transcript")
def get_transcript(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        return {"error": "Meeting not found"}

    if meeting.status == "processing":
        return {"status": "processing", "message": "Still processing, try again shortly"}

    if meeting.status == "failed":
        return {"status": "failed", "error": meeting.error_message}

    return {
        "status": "completed",
        "filename": meeting.filename,
        "duration_seconds": meeting.duration_seconds,
        "full_text": meeting.full_text,
        "transcript": json.loads(meeting.transcript_json)
    }