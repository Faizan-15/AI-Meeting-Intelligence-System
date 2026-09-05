# AI Meeting Intelligence — Transcription & Media Engine Module

Ye module Meeting Intelligence System ka core AI pipeline hai. Ye audio/video meeting
recordings ko leta hai, unhe text mein convert karta hai, speakers identify karta hai,
aur ek structured, speaker-wise transcript deta hai (timestamps ke saath).

## Ye Kya Karta Hai

1. Audio ya video file upload accept karta hai
2. Agar video hai, to FFmpeg se audio nikaalta hai
3. OpenAI Whisper se speech-to-text conversion karta hai (timestamps ke saath)
4. pyannote.audio se speaker diarization (kaun kab bola) karta hai
5. Dono ko merge kar ke ek clean, speaker-wise transcript banata hai
6. Result ko database (SQLite) mein save karta hai
7. Processing background mein chalti hai (lambi recordings ke liye)

## Technologies Used

- **Language:** Python
- **Framework:** FastAPI
- **Speech-to-Text:** OpenAI Whisper
- **Speaker Diarization:** pyannote.audio
- **Audio/Video Processing:** FFmpeg
- **Database:** SQLite (via SQLAlchemy)

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- FFmpeg installed aur system PATH mein add hona chahiye
- HuggingFace account + access token (pyannote models ke liye)

### 2. Installation

\`\`\`bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
\`\`\`

### 3. Environment Variables

Project root mein `.env` file banao:
\`\`\`
HUGGINGFACE_TOKEN=your_huggingface_token_here
\`\`\`

### 4. Run the Server

\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

Server: `http://127.0.0.1:8000`
API docs: `http://127.0.0.1:8000/docs`

## API Endpoints

### `POST /upload-meeting`
Audio/video file upload karta hai, background processing shuru karta hai.

### `GET /meeting/{meeting_id}/status`
Processing status check karta hai (processing/completed/failed).

### `GET /meeting/{meeting_id}/transcript`
Final speaker-wise transcript deta hai timestamps ke saath.

## Known Limitations

- Speaker diarization kabhi kabhi similar-sounding voices ko galat se ek hi
  speaker samajh sakta hai, khaaskar short (<15 second) recordings mein.
- Supported video formats: .mp4, .mov, .avi, .mkv