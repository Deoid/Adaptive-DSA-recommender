from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from backend.database import Base

class ProblemCatalog(Base):
    __tablename__ = "problem_catalog"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False, index=True) # codeforces, leetcode, atcoder, codechef
    problem_id = Column(String(100), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    canonical_topic = Column(String(100), nullable=False, index=True)
    tags = Column(String(500), nullable=True)
    difficulty = Column(Integer, nullable=False, index=True) # Elo difficulty (800 - 3200)
    acceptance_rate = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("platform", "problem_id", name="uq_platform_problem"),
    )
