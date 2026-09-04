import json

from services.llm_service import analyze_meeting
from schemas.meeting import MeetingAnalysis


transcript = """
Meeting date: September 3, 2026

Ali: We need to finish the website by Friday.

Sara: I will handle the frontend.

Ahmed: I will prepare the database.

Ali: Good. Let's review everything next Monday.
"""


try:
    result = analyze_meeting(transcript)

    data = json.loads(result)

    meeting = MeetingAnalysis.model_validate(data)

    print("\nVALIDATED MEETING ANALYSIS:\n")
    print(meeting.model_dump_json(indent=2))

except Exception as e:
    print(f"\nERROR: {e}")