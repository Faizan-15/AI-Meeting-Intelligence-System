import os
from dotenv import load_dotenv
from pyannote.audio import Pipeline

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    token=HF_TOKEN
)

def get_speaker_segments(audio_path, min_speakers=1, max_speakers=6):
    result = diarization_pipeline(audio_path, min_speakers=min_speakers, max_speakers=max_speakers)

    if hasattr(result, "speaker_diarization"):
        diarization = result.speaker_diarization
    else:
        diarization = result

    speaker_segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        speaker_segments.append({
            "speaker": speaker,
            "start": turn.start,
            "end": turn.end
        })

    return speaker_segments