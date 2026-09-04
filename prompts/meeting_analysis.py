MEETING_ANALYSIS_PROMPT = """
Analyze the meeting transcript below.

Extract the following information:
- Meeting title
- Short summary
- Participants
- Key discussion points
- Decisions made
- Action items
- Timestamp where the action item was mentioned
- Task owner for each action item
- Deadline for each action item
- Unresolved issues
- Follow-up items
- Overall meeting sentiment

Important rules:
1. Only use information present in the transcript.
2. Do not invent names, tasks, decisions, or deadlines.
3. If information is missing, return an empty list or null where appropriate.
4. Keep extracted information concise and clear.
5. Preserve the meaning of what was actually said.
6. Only include something in decisions_made if the participants explicitly agreed on, approved, selected, rejected, or finalized it.
7. Do not treat assigned tasks as decisions unless the transcript explicitly describes the task assignment as a decision.
8. Action items should contain tasks that someone is expected to complete.
9. The sentiment must be one of:
positive, neutral, negative, mixed.
10. The timestamp must be in the format "YYYY-MM-DD HH:MM:SS", or use the timestamp provided in the transcript.
Do not invent timestamps.

For each deadline:
- Preserve the original deadline phrase in "deadline".
- Convert relative deadlines into an exact date in "deadline_normalized" when the meeting date is available.
- Use YYYY-MM-DD format for normalized dates.
- If the meeting date is unavailable or the deadline cannot be determined, set deadline_normalized to null.
- Never guess a date.

Return the result using exactly these field names:

meeting_title
short_summary
participants
key_discussion_points
decisions_made
action_items
timestamp
unresolved_issues
follow_up_items
sentiment

Do not use different field names.
Return only valid JSON.

Meeting transcript:
{transcript}
"""