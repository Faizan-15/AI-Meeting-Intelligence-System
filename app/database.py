from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Database configuration - SQLite for local, PostgreSQL for cloud
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./meetings.db"
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    status = Column(String, default="processing")  # processing / completed / failed
    duration_seconds = Column(Float, nullable=True)
    full_text = Column(Text, nullable=True)
    transcript_json = Column(Text, nullable=True)  # poora transcript JSON string ke roop mein
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Tables ban jayengi jab app start hoga
def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()