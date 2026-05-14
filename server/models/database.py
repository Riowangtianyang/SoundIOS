from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from models import Base
from datetime import datetime


class Recording(Base):
    __tablename__ = "recordings"

    id = Column(Integer, primary_key=True, index=True)
    audio_path = Column(String(500), nullable=False)
    duration = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="pending")  # pending, processing, completed, failed

    transcript = relationship("Transcript", back_populates="recording", uselist=False)


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("recordings.id"), unique=True)
    text = Column(Text, nullable=False)
    segments = Column(JSON, nullable=True)

    recording = relationship("Recording", back_populates="transcript")


class DiaryEntry(Base):
    __tablename__ = "diary_entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text, nullable=False)
    details = Column(Text, nullable=True)
    mood_score = Column(Integer, nullable=True)  # 1-10


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Integer, default=3)  # 1-5, 1 is highest
    status = Column(String(50), default="pending")  # pending, in_progress, completed


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    relationship_type = Column(String(100), nullable=True)  # 避免与 SQLAlchemy relationship 方法冲突
    notes = Column(Text, nullable=True)
    personality_tags = Column(JSON, nullable=True)

    memories = relationship("Memory", back_populates="person")


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=True)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=True)  # conversation, event, preference, fact
    confirmed = Column(Integer, default=0)  # 0: unconfirmed, 1: confirmed

    person = relationship("Person", back_populates="memories")
