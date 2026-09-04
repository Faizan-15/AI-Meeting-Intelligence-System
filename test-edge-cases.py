import json

from services.qa_service import answer_question
from schemas.meeting import MeetingQA


transcript = """
[00:01] Ali: We need to finish the website by Friday.

[00:15] Sara: I will handle the frontend.

[00:30] Ahmed: I will prepare the database.

[00:45] Ali: Good. Let's review everything next Monday.
"""


questions = [
    "Who will prepare the database?",
    "Who will handle the marketing?",
    "What is the budget for the project?"
]


for question in questions:

    print(f"\nQUESTION: {question}")

    try:
        result = answer_question(transcript, question)

        data = json.loads(result)

        qa = MeetingQA.model_validate(data)

        print(qa.model_dump_json(indent=2))

    except Exception as e:
        print(f"ERROR: {e}")