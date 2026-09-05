from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi import Depends
import shutil
import os
import json

from app.transcribe import convert_video_to_audio, transcribe_audio
from app.diarize import get_speaker_segments
from app.merge import merge_transcript_with_speakers
from app.database import init_db, get_db, Meeting

app = FastAPI()

UPLOAD_DIR = "uploads"
VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv"]


@app.on_event("startup")
def on_startup():
    init_db()  # App start hote hi database tables ban jayengi


@app.get("/")
def home():
    return {"message": "Transcription Module is running"}


def process_meeting(meeting_id: int, file_path: str, filename: str):
    """Background mein chalne wala function - poora processing yahan hoti hai"""
    db = next(get_db())
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    try:
        ext = os.path.splitext(filename)[1].lower()

        if ext in VIDEO_EXTENSIONS:
            audio_path = os.path.join(UPLOAD_DIR, f"audio_{meeting_id}.wav")
            convert_video_to_audio(file_path, audio_path)
        else:
            audio_path = file_path

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
        # Agar kahin error aaye, status "failed" kar do
        meeting.status = "failed"
        meeting.error_message = str(e)
        db.commit()

    finally:
        db.close()


@app.post("/upload-meeting")
async def upload_meeting(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Database mein ek naya record banao, status = "processing"
    new_meeting = Meeting(filename=file.filename, status="processing")
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    # Processing background mein chalao (turant response wapas chala jayega)
    background_tasks.add_task(process_meeting, new_meeting.id, file_path, file.filename)

    return {
        "message": "File uploaded, processing started",
        "meeting_id": new_meeting.id,
        "status": "processing"
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