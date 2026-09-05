import whisper
import ffmpeg
import os

# Whisper model ek baar load karo (baar baar load na ho isliye yahan global rakha)
model = whisper.load_model("base")

def convert_video_to_audio(input_path, output_path):
    """Agar file video hai to usay audio (.wav) mein convert karega"""
    ffmpeg.input(input_path).output(output_path, ac=1, ar=16000).run(overwrite_output=True)
    return output_path

def transcribe_audio(audio_path):
    """Whisper se audio ko text mein convert karega, timestamps ke sath"""
    result = model.transcribe(audio_path, word_timestamps=True)
    return result