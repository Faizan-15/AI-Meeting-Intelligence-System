from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, text
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer
import helpiings as s
import requests
import json

# 1. Database Connection & Setup
DATABASE_URL = "postgresql://user:password@localhost:5432/meeting_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

with engine.connect() as connection:
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    connection.commit()

class TranscriptChunk(Base):
    __tablename__ = "transcript_chunks"
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, index=True)
    text_content = Column(Text)
    start_timestamp = Column(String) 
    embedding = Column(Vector(384)) 

Base.metadata.create_all(bind=engine)

# 2. FastAPI & Local Embeddings Initialization
app = FastAPI()
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Define your API Key here directly
GEMINI_API_KEY = s.API_KEY

class QuestionRequest(BaseModel):
    meeting_id: str
    question: str

# 3. Core AI Search & Answer Endpoint
@app.post("/api/ask")
def ask_ai(request: QuestionRequest):
    db = SessionLocal()
    try:
        # Step A: Generate local vector
        question_embedding = embedder.encode(request.question).tolist()

        # Step B: Search DB
        results = db.query(TranscriptChunk).filter(
            TranscriptChunk.meeting_id == request.meeting_id
        ).order_by(
            TranscriptChunk.embedding.cosine_distance(question_embedding)
        ).limit(3).all()

        # Step C: Context block
        context_text = "\n".join([f"[{r.start_timestamp}] {r.text_content}" for r in results])

        # Step D: Prompt Engineering
        prompt = f"""
        Role: You are an expert Meeting Intelligence Assistant.
        Task: Answer the user's question using ONLY the provided meeting context.
        
        Context:
        {context_text}
        
        Instructions:
        - Base your answer strictly on the context above.
        - You MUST include the exact timestamp reference from the context.
        - Format your response as JSON with "answer" and "timestamp_reference" keys.
        
        User Question: {request.question}
        """

        # Step E: Generate final answer via Direct HTTP Request (Using an authorized 2026 model)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
        response_data = response.json()
        
        # Safety catch: If Google's API throws a raw error, return it cleanly without a 500 crash
        if "error" in response_data:
            return {"api_error": response_data["error"]["message"]}

        # Extract the text from the raw JSON response
        raw_answer = response_data['candidates'][0]['content']['parts'][0]['text']
        
        # Strip any markdown formatting
        clean_answer = raw_answer.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_answer)
    finally:
        db.close()