from datetime import date

from schemas.meeting import ActionItem
from services.deadline_service import normalize_deadline


meeting_date = date(2026, 9, 3)


action_items = [
    ActionItem(
        task="Finish the website",
        owner="Ali",
        deadline="Friday"
    ),
    ActionItem(
        task="Prepare the database",
        owner="Ahmed",
        deadline="September 10"
    ),
    ActionItem(
        task="Review everything",
        owner="Ali",
        deadline="Next Monday"
    ),
    ActionItem(
        task="Complete documentation",
        owner="Sara",
        deadline="end of month"
    )
]


for action in action_items:
    action.deadline_normalized = normalize_deadline(
        action.deadline,
        meeting_date
    )


print("\nDEADLINE INTEGRATION TEST:\n")

for action in action_items:
    print(action.model_dump_json(indent=2))