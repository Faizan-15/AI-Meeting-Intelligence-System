# AI Meeting Intelligence System

An AI-powered meeting analysis pipeline that converts meeting transcripts into structured and actionable information.

## Overview

The AI pipeline uses Google Gemini to analyze a meeting transcript and extract:

- Meeting title
- Short summary
- Participants
- Key discussion points
- Decisions made
- Action items
- Task owners
- Deadlines
- Normalized deadlines
- Unresolved issues
- Follow-up items
- Overall meeting sentiment
- Timestamps for relevant action items and Q&A answers

The pipeline is designed to return structured JSON instead of free-form text so that the extracted meeting data can be validated and consumed by other parts of the application.

## AI Pipeline Flow

```text
Meeting Transcript
        |
        v
Prompt Engineering
        |
        v
Google Gemini
        |
        v
Structured JSON Response
        |
        v
Pydantic Validation
        |
        +------> Action Items
        |          |
        |          v
        |    Deadline Normalization
        |
        v
Validated Meeting Data
```

## Project Structure

```text
meeting-intelligence-ai/
|
├── prompts/
│   ├── meeting_analysis.py
│   └── meeting_qa.py
|
├── schemas/
│   └── meeting.py
|
├── services/
│   ├── llm_service.py
│   ├── deadline_service.py
│   └── qa_service.py
|
├── test-analysis.py
├── test-deadline.py
├── test-deadline-integration.py
├── test-qa.py
├── test-edge-cases.py
│
├── requirements.txt
├── .gitignore
└── .env
```

## Requirements

- Python 3.10+
- Google Gemini API key
- Packages listed in `requirements.txt`

The main packages used by the AI pipeline are:

- `google-genai`
- `pydantic`
- `python-dotenv`

## Environment Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit `.env` or expose the API key.

The repository `.gitignore` excludes:

```text
venv/
.env
__pycache__/
*.pyc
```

## Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Meeting Analysis

The main analysis function is:

```python
from services.llm_service import analyze_meeting

result = analyze_meeting(transcript)
```

The service:

1. Checks that the transcript is not empty.
2. Inserts the transcript into the meeting-analysis prompt.
3. Sends the prompt to Gemini.
4. Requests JSON output.
5. Parses the JSON response.
6. Validates the response using the `MeetingAnalysis` Pydantic model.
7. Extracts the meeting date when available.
8. Normalizes action-item deadlines using the deadline service.
9. Returns validated JSON.

## Structured Data Models

### `MeetingAnalysis`

Contains the main meeting-level information:

- `meeting_title`
- `short_summary`
- `participants`
- `key_discussion_points`
- `decisions_made`
- `action_items`
- `unresolved_issues`
- `follow_up_items`
- `sentiment`

### `ActionItem`

Each action item contains:

- `task`
- `owner`
- `deadline`
- `deadline_normalized`
- `timestamp`

### `MeetingQA`

Q&A responses contain:

- `answer`
- `timestamp`

## Deadline Normalization

The deadline service converts common natural-language deadlines into `YYYY-MM-DD` dates when the meeting date is known.

Examples:

| Input | Example normalized result |
|---|---|
| `Friday` | `2026-09-04` |
| `Tomorrow` | `2026-09-04` |
| `Monday` | `2026-09-07` |
| `Next Monday` | `2026-09-07` |
| `September 10` | `2026-09-10` |
| `end of month` | `2026-09-30` |

If a deadline cannot be determined safely, the service returns `None` rather than guessing.

## Meeting Q&A

The Q&A service answers questions using only the supplied meeting transcript.

Example:

```python
from services.qa_service import answer_question

result = answer_question(
    transcript,
    "Who will prepare the database?"
)
```

The expected structured response contains the answer and, when available, the timestamp of the relevant statement.

## Hallucination Prevention

The prompts explicitly instruct the model to:

- Use only information present in the transcript.
- Never invent names, tasks, decisions, deadlines, or timestamps.
- Return empty lists or `null` when information is unavailable.
- Preserve the meaning of the transcript.
- Treat only explicitly agreed, approved, selected, rejected, or finalized items as decisions.
- Keep action items limited to tasks someone is expected to complete.

For Q&A, questions that cannot be answered from the transcript should return that the information is not available.

## Testing

### Meeting analysis

```powershell
python test-analysis.py
```

This test calls Gemini, parses the JSON response, and validates it with `MeetingAnalysis`.

### Deadline unit tests

```powershell
python test-deadline.py
```

This test runs locally and does not require a Gemini API call.

### Deadline integration test

```powershell
python test-deadline-integration.py
```

This verifies that normalized deadlines can be assigned to validated `ActionItem` objects.

### Q&A test

```powershell
python test-qa.py
```

This calls Gemini and validates the response using `MeetingQA`.

### Q&A edge cases

```powershell
python test-edge-cases.py
```

This checks both answerable and unavailable questions.

## Important Notes

- Gemini API tests consume API quota. Avoid repeatedly running the Gemini-dependent tests when quota is limited.
- Deadline normalization is deterministic Python logic and can be tested without Gemini.
- The LLM is responsible for extracting the original deadline phrase; the Python deadline service handles deterministic normalization.
- API keys must remain outside source control.

## Current AI Pipeline Scope

This repository's AI pipeline focuses on prompt engineering, structured extraction, validation, deadline normalization, meeting Q&A, timestamp handling, and extraction quality controls.
