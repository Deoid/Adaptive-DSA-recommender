from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Connected Platform Handles
    codeforces_handle = Column(String(100), nullable=True)
    leetcode_handle = Column(String(100), nullable=True)
    codechef_handle = Column(String(100), nullable=True)
    atcoder_handle = Column(String(100), nullable=True)

    target_rating = Column(Integer, default=1600)
    user_overall_elo = Column(Integer, default=1200)

    # Relationships
    submissions = relationship("UserSubmission", back_populates="user", cascade="all, delete-orphan")
    mastery_states = relationship("TopicMasteryState", back_populates="user", cascade="all, delete-orphan")
