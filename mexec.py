from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Text, text
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector

# 1. Connect to the Docker database we just started
DATABASE_URL = "postgresql://user:password@localhost:5432/meeting_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---> NEW STEP: Enable the pgvector extension inside the database first <---
with engine.connect() as connection:
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    connection.commit()

# 2. Define the exact table structure for the meeting transcripts
class TranscriptChunk(Base):
    __tablename__ = "transcript_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, index=True)
    text_content = Column(Text)
    start_timestamp = Column(String) 
    embedding = Column(Vector(1536)) # This holds the AI math numbers

# 3. Create the table in the database
Base.metadata.create_all(bind=engine)

# 4. Initialize the FastAPI web server
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Vector Database Connected Successfully!"}