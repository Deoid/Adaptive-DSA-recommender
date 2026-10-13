from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.database import Base

class TopicMasteryState(Base):
    __tablename__ = "topic_mastery_states"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = Column(String(100), nullable=False, index=True)
    
    # Bayesian Knowledge Tracing metrics
    mastery_probability = Column(Float, nullable=False, default=0.15) # P(L)
    prior_probability = Column(Float, nullable=False, default=0.15)   # P(L0)
    total_attempts = Column(Integer, nullable=False, default=0)
    correct_attempts = Column(Integer, nullable=False, default=0)
    recent_window_accuracy = Column(Float, nullable=False, default=0.0)
    
    # Elo skill estimation for this topic
    topic_elo = Column(Float, nullable=False, default=1200.0)

    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "topic", name="uq_user_topic_mastery"),
    )

    user = relationship("User", back_populates="mastery_states")
