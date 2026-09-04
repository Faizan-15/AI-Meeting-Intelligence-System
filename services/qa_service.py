import os
from dotenv import load_dotenv
from google import genai

from prompts.meeting_qa import MEETING_QA_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def answer_question(transcript: str, question: str):

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    prompt = MEETING_QA_PROMPT.format(
        transcript=transcript,
        question=question
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text