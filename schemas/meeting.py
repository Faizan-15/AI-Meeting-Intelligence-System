from typing import Optional
from pydantic import BaseModel


class ActionItem(BaseModel):
    task: str
    owner: Optional[str] = None
    deadline: Optional[str] = None
    deadline_normalized: Optional[str] = None
    timestamp: Optional[str] = None

class MeetingQA(BaseModel):
    answer: str
    timestamp: Optional[str] = None

class MeetingAnalysis(BaseModel):
    meeting_title: Optional[str] = None
    short_summary: str
    participants: list[str]
    key_discussion_points: list[str]
    decisions_made: list[str]
    action_items: list[ActionItem]
    unresolved_issues: list[str]
    follow_up_items: list[str]
    sentiment: Optional[str] = None