MEETING_QA_PROMPT = """
Answer the user's question using only the meeting transcript below.

Rules:
1. Use only information present in the transcript.
2. Do not invent or assume information.
3. If the answer cannot be found in the transcript, say that the information is not available.
4. Keep the answer concise and clear.
5. If the answer is related to a specific statement, include its timestamp when a timestamp is available.
6. Do not create or guess timestamps.

Return valid JSON using exactly these fields:

answer
timestamp

Meeting transcript:
{transcript}

User question:
{question}
"""