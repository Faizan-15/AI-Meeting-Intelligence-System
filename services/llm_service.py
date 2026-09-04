import json
import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai

from prompts.meeting_analysis import MEETING_ANALYSIS_PROMPT
from schemas.meeting import MeetingAnalysis
from services.deadline_service import normalize_deadline


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_meeting(transcript: str):

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    prompt = MEETING_ANALYSIS_PROMPT.format(
        transcript=transcript
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        data = json.loads(response.text)

        meeting = MeetingAnalysis.model_validate(data)

        meeting_date = None

        for line in transcript.splitlines():
            if line.lower().startswith("meeting date:"):
                date_text = line.split(":", 1)[1].strip()

                try:
                    meeting_date = datetime.strptime(
                        date_text,
                        "%B %d, %Y"
                    ).date()
                except ValueError:
                    pass

                break

        if meeting_date:
            for action in meeting.action_items:
                if action.deadline:
                    action.deadline_normalized = normalize_deadline(
                        action.deadline,
                        meeting_date
                    )

        return meeting.model_dump_json()

    except Exception as e:
        raise RuntimeError(
            f"Meeting analysis failed: {e}"
        ) from e