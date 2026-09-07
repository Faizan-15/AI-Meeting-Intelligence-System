# AI-Meeting-Intelligence-System

AI-powered Meeting Intelligence System that transforms meeting audio/video into structured insights, including summaries, speaker-wise transcripts, decisions, action items, deadlines, unresolved issues, and contextual AI-powered Q&A.

## Architecture & Tech Stack

* **Backend Framework:** FastAPI (Python)
* **Vector Database:** PostgreSQL with the `pgvector` extension
* **Local Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2` / 384-d)
* **LLM Engine:** Google Gemini REST API (`gemini-3.6-flash`) bypassed via direct HTTP for high stability.
* **ORM:** SQLAlchemy + pgvector-python

## Local Setup Instructions

Follow these steps to set up the Python vector database environment locally:

1. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment:**
    
    On Windows (Powershell):
    ```bash
    .\venv\Scripts\activate
    ```
    On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Start the PostgreSQL Vector Database (Docker required):**

    To initialize the database for the first time:
    ```bash
    docker run --name pgvector-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=meeting_db -p 5432:5432 -d ankane/pgvector
    ```
    *(For future runs, you only need to run: `docker start pgvector-db`)*

5. **Seed the Database:**
    Generate local embeddings and populate the database with initial meeting transcripts:
    ```bash
    python seed.py
    ```

6. **Set Environment Variables:**
    To satisfy GitHub Push Protection and keep your credentials secure, set your Gemini API key directly in your active terminal:
    
    * **Windows (PowerShell):**
      ```powershell
      $env:GEMINI_API_KEY="your_actual_api_key_here"
      ```
    * **macOS / Linux:**
      ```bash
      export GEMINI_API_KEY="your_actual_api_key_here"
      ```

7. **Run the FastAPI server:**
    ```bash
    uvicorn mexec:app --reload
    ```
    *Note: Ensure your virtual environment is active before running the server. You can access the API at http://127.0.0.1:8000.*

## Testing the API

Once the server is running, navigate to the Swagger UI at `http://127.0.0.1:8000/docs`. You can test the hallucination-proof RAG pipeline by executing a `POST` request on the `/api/ask` endpoint with a target `meeting_id` and `question`.