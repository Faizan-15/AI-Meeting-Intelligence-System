# AI Pipeline Documentation

## 1. Purpose

The AI Pipeline transforms a meeting transcript into structured meeting intelligence.

The pipeline is responsible for the LLM-facing and data-extraction layer rather than the frontend or general application UI.

Its main responsibilities are:

1. Prompt engineering
2. Structured extraction
3. Pydantic validation
4. Action-item extraction
5. Owner and deadline extraction
6. Deadline normalization
7. Decision extraction
8. Summary and discussion-point extraction
9. Sentiment extraction
10. Timestamp handling
11. Meeting Q&A
12. Missing-data and hallucination controls

---

## 2. Analysis Prompt

The meeting-analysis prompt is defined in:

```text
prompts/meeting_analysis.py
```

The prompt asks Gemini to extract meeting-level and action-item information from the transcript.

The requested fields include:

```text
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
```

The prompt also provides extraction rules to reduce hallucination and preserve the meaning of the transcript.

### Key prompt rules

The model is instructed to:

- Use only information present in the transcript.
- Never invent names, tasks, decisions, deadlines, or timestamps.
- Return empty lists or `null` when information is missing.
- Keep extracted information concise.
- Preserve the original meaning.
- Only classify something as a decision when it was explicitly agreed, approved, selected, rejected, or finalized.
- Avoid treating a normal task assignment as a decision.
- Extract action items as tasks someone is expected to complete.
- Preserve the original deadline phrase.
- Avoid guessing normalized dates.
- Use one of four sentiment values:
  - `positive`
  - `neutral`
  - `negative`
  - `mixed`

---

## 3. Structured Schema

The data models are defined in:

```text
schemas/meeting.py
```

Pydantic is used to validate the LLM response before the data is returned to the rest of the system.

### ActionItem

```text
task
owner
deadline
deadline_normalized
timestamp
```

`owner`, `deadline`, `deadline_normalized`, and `timestamp` are optional because meeting transcripts may not contain all of this information.

### MeetingAnalysis

```text
meeting_title
short_summary
participants
key_discussion_points
decisions_made
action_items
unresolved_issues
follow_up_items
sentiment
```

### MeetingQA

```text
answer
timestamp
```

---

## 4. LLM Service

The main meeting-analysis service is:

```text
services/llm_service.py
```

### Processing sequence

```text
Transcript
   |
   v
Empty-input validation
   |
   v
Analysis prompt construction
   |
   v
Gemini request
   |
   v
JSON response
   |
   v
JSON parsing
   |
   v
Pydantic validation
   |
   v
Meeting date extraction
   |
   v
Deadline normalization
   |
   v
Validated JSON output
```

The service uses:

```text
gemini-3.6-flash
```

and requests JSON output through the Gemini configuration.

---

## 5. Deadline Normalization

The deadline logic is implemented in:

```text
services/deadline_service.py
```

The LLM extracts the original phrase, for example:

```text
Friday
Tomorrow
Next Monday
September 10
end of month
```

Python then converts the phrase to an exact date when the meeting date is known.

### Supported cases

#### Weekdays

A weekday such as:

```text
Friday
Monday
```

is converted to the next occurrence after the meeting date.

#### Next weekday

For example:

```text
Next Monday
```

is converted to the following Monday.

#### Tomorrow

```text
Tomorrow
```

is converted to one day after the meeting date.

#### End of month

```text
end of month
end of the month
```

is converted to the last calendar day of the meeting month.

#### Explicit month/day

Examples:

```text
September 10
Sep 10
```

are converted using the meeting year.

### Safety behavior

If the deadline is empty or unsupported, the service returns:

```python
None
```

instead of guessing.

---

## 6. Meeting Q&A

Q&A is implemented in:

```text
services/qa_service.py
```

The prompt is defined in:

```text
prompts/meeting_qa.py
```

The service receives:

```text
meeting transcript
question
```

and asks Gemini to answer using only the transcript.

The response is expected to contain:

```json
{
  "answer": "...",
  "timestamp": "..."
}
```

### Q&A rules

The model must:

- Use only transcript information.
- Never invent or assume information.
- State that information is not available when the transcript does not contain an answer.
- Keep answers concise.
- Include a timestamp when the relevant statement has one.
- Never guess timestamps.

---

## 7. Timestamp Handling

Timestamps are preserved when available in the source transcript.

For action items, timestamps are stored on the `ActionItem`.

For Q&A, the `MeetingQA` model contains the timestamp of the relevant statement.

The pipeline does not intentionally generate timestamps that are not present in the input.

---

## 8. Decision Extraction

Decision extraction is deliberately stricter than general discussion extraction.

An item should be included in `decisions_made` only when the transcript indicates that participants explicitly:

- agreed
- approved
- selected
- rejected
- finalized

A task assignment by itself is not treated as a decision.

This separation helps distinguish:

```text
Discussion
    |
    +--> Decision
    |
    +--> Action Item
    |
    +--> Follow-up
```

---

## 9. Action-Item Extraction

Action items represent work that someone is expected to complete.

Each action item can contain:

```text
task
owner
deadline
deadline_normalized
timestamp
```

Example:

```json
{
  "task": "Prepare the database",
  "owner": "Ahmed",
  "deadline": "Friday",
  "deadline_normalized": "2026-09-04",
  "timestamp": null
}
```

The original deadline phrase is preserved while the normalized deadline provides a machine-friendly date.

---

## 10. Sentiment

The meeting-analysis prompt restricts sentiment to:

```text
positive
neutral
negative
mixed
```

The value is optional in the schema so that missing model output does not automatically create invalid data.

---

## 11. Validation Strategy

The pipeline does not directly trust raw LLM output.

The process is:

```text
Gemini JSON
     |
     v
json.loads()
     |
     v
MeetingAnalysis.model_validate()
     |
     v
Validated Pydantic object
     |
     v
model_dump_json()
```

This provides a structural validation layer between the LLM and downstream application components.

---

## 12. Error Handling

The analysis service checks for:

- Empty transcripts
- Empty Gemini responses
- Invalid JSON
- Schema validation failures
- Other analysis errors

The service raises a descriptive `RuntimeError` when the analysis pipeline fails.

The Q&A service separately validates:

- Empty transcript
- Empty question
- Empty Gemini response

---

## 13. Tests

### `test-analysis.py`

Tests the complete Gemini-based meeting-analysis flow and Pydantic validation.

### `test-deadline.py`

Tests individual deadline normalization cases without using Gemini.

### `test-deadline-integration.py`

Tests deadline normalization together with the `ActionItem` Pydantic model.

Verified cases include:

```text
Friday          -> 2026-09-04
September 10    -> 2026-09-10
Next Monday     -> 2026-09-07
end of month    -> 2026-09-30
```

### `test-qa.py`

Tests a normal meeting Q&A request and validates it with `MeetingQA`.

### `test-edge-cases.py`

Tests questions for:

- Information that exists in the transcript
- Information that does not exist
- Questions where no answer should be invented

---

## 14. Security and Data Handling

The Gemini API key is loaded through an environment variable:

```text
GEMINI_API_KEY
```

The `.env` file is excluded from Git using `.gitignore`.

Never place an API key directly inside Python source code or documentation.

---

## 15. Design Principle

The core design principle is:

> Let the LLM extract meaning, but keep deterministic transformations in Python whenever possible.

For example:

```text
LLM:
"Friday"

Python:
"2026-09-04"
```

This reduces dependence on the LLM for deterministic date calculations and makes deadline normalization easier to test.

---

## 16. Current Limitations

The current implementation is focused on transcript-based AI processing.

The deadline normalizer currently handles:

- Weekdays
- `next <weekday>`
- `tomorrow`
- End of month
- Month/day expressions

Unsupported or ambiguous deadline phrases return `None` rather than being guessed.

The meeting-date parser currently expects the transcript date in:

```text
Meeting date: September 3, 2026
```

format.

---

## 17. Future Extensions

Potential future improvements include:

- More natural-language deadline patterns
- More robust date parsing
- Additional timestamp formats
- Better normalization for dates containing years
- More extensive automated evaluation datasets
- Confidence or extraction-quality metrics
- Retrieval-based Q&A over long meetings
