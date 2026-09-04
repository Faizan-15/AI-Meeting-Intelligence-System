from sentence_transformers import SentenceTransformer
from mexec import SessionLocal, TranscriptChunk

# Downloads a tiny, fast, free local model (only happens once)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

dummy_transcripts = [
    {"meeting_id": "meet_001", "time": "14:00", "text": "Faizan: We need to finalize the AI architecture for the internship project today."},
    {"meeting_id": "meet_001", "time": "14:05", "text": "Zeeshan: I will finish the backend database by Friday."},
    {"meeting_id": "meet_001", "time": "14:10", "text": "Sara: I am assigned to complete the frontend React components."}
]

def seed_database():
    db = SessionLocal()
    print("Generating local vectors and saving to database...")
    
    for item in dummy_transcripts:
        # Generate the math locally
        embedding = embedder.encode(item["text"]).tolist()
        
        new_chunk = TranscriptChunk(
            meeting_id=item["meeting_id"],
            text_content=item["text"],
            start_timestamp=item["time"],
            embedding=embedding
        )
        db.add(new_chunk)
    
    db.commit()
    db.close()
    print("Success! Sample transcripts added to the Vector Database.")

if __name__ == "__main__":
    seed_database()