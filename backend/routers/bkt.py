from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_db
from backend.models.user import User
from backend.models.submission import UserSubmission
from backend.models.bkt_state import TopicMasteryState
from backend.auth.dependencies import get_current_user
from backend.services.bkt_model import bkt_engine
from backend.services.elo_matcher import elo_matcher
from backend.services.canonical_topics import CANONICAL_TOPICS

router = APIRouter(prefix="/bkt", tags=["Bayesian Knowledge Tracing"])

class SubmitVerdictRequest(BaseModel):
    topic: str
    problem_id: str
    problem_title: str
    platform: str = "practice"
    difficulty: int = 1400
    is_accepted: bool

class SimulateBktRequest(BaseModel):
    initial_p_l: float = 0.15
    verdicts: List[bool] # list of True (AC) or False (WA)
    user_elo: float = 1200.0
    problem_difficulty: float = 1400.0

@router.get("/mastery")
async def get_mastery_vector(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns the user's estimated skill probability P(L) for each DSA topic,
    along with Elo ratings and sliding window accuracy.
    """
    states_res = await db.execute(
        select(TopicMasteryState).where(TopicMasteryState.user_id == current_user.id)
    )
    states = states_res.scalars().all()
    states_dict = {s.topic: s for s in states}

    vector = []
    for topic in CANONICAL_TOPICS:
        state = states_dict.get(topic)
        p_l = state.mastery_probability if state else 0.15
        elo = state.topic_elo if state else float(current_user.user_overall_elo or 1200)
        attempts = state.total_attempts if state else 0
        correct = state.correct_attempts if state else 0
        acc = state.recent_window_accuracy if state else 0.0

        if p_l >= 0.80:
            status = "Mastered"
        elif p_l >= 0.60:
            status = "Competent"
        elif p_l >= 0.35:
            status = "Developing"
        else:
            status = "Novice"

        vector.append({
            "topic": topic,
            "mastery_probability": round(p_l, 4),
            "mastery_percentage": round(p_l * 100, 1),
            "topic_elo": round(elo, 1),
            "total_attempts": attempts,
            "correct_attempts": correct,
            "recent_accuracy": round(acc, 3),
            "status": status,
        })

    return {
        "user_id": current_user.id,
        "overall_elo": current_user.user_overall_elo,
        "topics": vector,
    }

@router.post("/submit-verdict")
async def submit_verdict(
    req: SubmitVerdictRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Updates the solver's estimated skill probability for the DSA topic
    after an Accepted or Wrong-Answer verdict, recalculating BKT and Elo.
    """
    if req.topic not in CANONICAL_TOPICS:
        raise HTTPException(status_code=400, detail=f"Invalid topic. Must be one of: {CANONICAL_TOPICS}")

    # 1. Log submission
    submission = UserSubmission(
        user_id=current_user.id,
        platform=req.platform,
        problem_id=req.problem_id,
        problem_title=req.problem_title,
        canonical_topic=req.topic,
        verdict="AC" if req.is_accepted else "WA",
        is_accepted=req.is_accepted,
        difficulty=req.difficulty,
        submission_time=datetime.utcnow(),
    )
    db.add(submission)

    # 2. Query last 20 submissions for this topic to run sliding window BKT
    res = await db.execute(
        select(UserSubmission)
        .where(UserSubmission.user_id == current_user.id, UserSubmission.canonical_topic == req.topic)
        .order_by(UserSubmission.submission_time.asc())
    )
    existing_subs = res.scalars().all()
    # include this new one
    verdicts = [s.is_accepted for s in existing_subs] + [req.is_accepted]

    bkt_res = bkt_engine.compute_from_submissions(verdicts, initial_prior=0.15)

    # 3. Update topic Elo
    state_res = await db.execute(
        select(TopicMasteryState).where(
            TopicMasteryState.user_id == current_user.id,
            TopicMasteryState.topic == req.topic
        )
    )
    state = state_res.scalar_one_or_none()
    old_elo = state.topic_elo if state else float(current_user.user_overall_elo or 1200)
    new_elo = elo_matcher.update_user_elo(old_elo, req.difficulty, req.is_accepted)

    if not state:
        state = TopicMasteryState(
            user_id=current_user.id,
            topic=req.topic,
            mastery_probability=bkt_res["mastery_probability"],
            prior_probability=0.15,
            total_attempts=len(verdicts),
            correct_attempts=sum(1 for v in verdicts if v),
            recent_window_accuracy=bkt_res["window_accuracy"],
            topic_elo=new_elo,
        )
        db.add(state)
    else:
        state.mastery_probability = bkt_res["mastery_probability"]
        state.total_attempts = len(verdicts)
        state.correct_attempts = sum(1 for v in verdicts if v)
        state.recent_window_accuracy = bkt_res["window_accuracy"]
        state.topic_elo = new_elo
        state.last_updated = datetime.utcnow()

    # Also update overall Elo slightly
    current_user.user_overall_elo = round(
        elo_matcher.update_user_elo(current_user.user_overall_elo or 1200, req.difficulty, req.is_accepted)
    )

    await db.commit()

    return {
        "status": "success",
        "topic": req.topic,
        "is_accepted": req.is_accepted,
        "previous_elo": round(old_elo, 1),
        "new_topic_elo": round(new_elo, 1),
        "new_mastery_probability": bkt_res["mastery_probability"],
        "mastery_status": bkt_res["status"],
        "window_accuracy": bkt_res["window_accuracy"],
        "submissions_in_sliding_window": bkt_res["submissions_analyzed"],
    }

@router.post("/simulate")
async def simulate_bkt(req: SimulateBktRequest):
    """
    Simulation sandbox: Computes BKT step transitions and Elo shifts
    across a sequence of hypothetical problem verdicts.
    """
    res = bkt_engine.compute_from_submissions(req.verdicts, initial_prior=req.initial_p_l)
    
    current_elo = req.user_elo
    elo_steps = [current_elo]
    for v in req.verdicts:
        current_elo = elo_matcher.update_user_elo(current_elo, req.problem_difficulty, v)
        elo_steps.append(current_elo)

    zpd = elo_matcher.evaluate_problem_fit(current_elo, req.problem_difficulty)

    return {
        "bkt_result": res,
        "elo_progression": elo_steps,
        "final_elo": current_elo,
        "zpd_evaluation": zpd,
    }
