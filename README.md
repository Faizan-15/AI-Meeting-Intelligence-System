# AI-Meeting-Intelligence-System
AI-powered Meeting Intelligence System that transforms meeting audio/video into structured insights, including summaries, speaker-wise transcripts, decisions, action items, deadlines, unresolved issues, and contextual AI-powered Q&A.

## Local Setup Instructions

Follow these steps to set up the Python vector database environment locally:

1. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment:**
    
    On Windows (Powershell):

        .\venv\Scripts\activate

    On macOS/Linux:

        source venv/bin/activate

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Start the PostgreSQL Vector Database (Docker required):**

    ```bash
    docker run --name pgvector-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=meeting_db -p 5432:5432 -d ankane/pgvector
    ```

5. **Run the FastAPI server:**
    ```bash
    uvicorn mexec:app --reload
    ```
    *Note: Ensure your virtual environment is active before running the server. You can access the API at http://127.0.0.1:8000.*
