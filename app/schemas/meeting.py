from typing import Optional, List
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
    participants: List[str]
    key_discussion_points: List[str]
    decisions_made: List[str]
    action_items: List[ActionItem]
    unresolved_issues: List[str]
    follow_up_items: List[str]
    sentiment: Optional[str] = None