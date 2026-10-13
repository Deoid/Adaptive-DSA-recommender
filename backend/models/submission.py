from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class UserSubmission(Base):
    __tablename__ = "user_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    platform = Column(String(50), nullable=False) # codeforces, leetcode, codechef, atcoder, manual
    problem_id = Column(String(100), nullable=False, index=True)
    problem_title = Column(String(255), nullable=False)
    canonical_topic = Column(String(100), nullable=False, index=True)
    platform_tags = Column(String(500), nullable=True)
    verdict = Column(String(50), nullable=False) # AC, WA, TLE, MLE, etc.
    is_accepted = Column(Boolean, nullable=False, default=False)
    difficulty = Column(Integer, nullable=True) # Elo or rating
    submission_time = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="submissions")
