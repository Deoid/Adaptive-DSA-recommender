from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_db
from backend.models.user import User
from backend.models.problem import ProblemCatalog
from backend.models.bkt_state import TopicMasteryState
from backend.models.submission import UserSubmission
from backend.auth.dependencies import get_current_user
from backend.services.ranking_engine import recommendation_engine
from backend.services.canonical_topics import CANONICAL_TOPICS

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("")
async def get_recommendations(
    mode: str = Query("balanced", description="Focus mode: 'balanced', 'weakness_focus', or 'rating_push'"),
    topic: Optional[str] = Query(None, description="Filter to a specific canonical DSA topic"),
    platform: Optional[str] = Query(None, description="Filter to a specific platform (e.g. codeforces, leetcode, atcoder, codechef)"),
    limit: int = Query(12, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Adaptive DSA Recommendation Engine endpoint:
    - Merges BKT mastery vector with Elo-based difficulty matching layer.
    - Excludes already-solved problems across all linked platforms.
    - Surfaces the problem set that maximizes solver cognitive growth.
    """
    # 1. Fetch user's BKT mastery vector and topic Elos
    states_res = await db.execute(
        select(TopicMasteryState).where(TopicMasteryState.user_id == current_user.id)
    )
    states = states_res.scalars().all()
    
    mastery_vector = {}
    topic_elo_map = {}
    overall_elo = float(current_user.user_overall_elo or 1200)

    for t in CANONICAL_TOPICS:
        mastery_vector[t] = 0.15
        topic_elo_map[t] = overall_elo

    for s in states:
        mastery_vector[s.topic] = s.mastery_probability
        topic_elo_map[s.topic] = s.topic_elo

    # 2. Fetch solved problem identifiers for deduplication
    solved_res = await db.execute(
        select(UserSubmission.problem_id, UserSubmission.platform)
        .where(UserSubmission.user_id == current_user.id, UserSubmission.is_accepted == True)
    )
    solved_keys = set()
    for row in solved_res.fetchall():
        solved_keys.add(str(row[0]))
        solved_keys.add(f"{row[1]}:{row[0]}")

    # 3. Fetch candidate problem pool
    query = select(ProblemCatalog)
    if platform and platform.lower() != "all":
        query = query.where(ProblemCatalog.platform == platform.lower())
    if topic:
        query = query.where(ProblemCatalog.canonical_topic == topic)

    problems_res = await db.execute(query)
    catalog_problems = problems_res.scalars().all()

    candidates = [
        {
            "id": p.id,
            "problem_id": p.problem_id,
            "platform": p.platform,
            "title": p.title,
            "url": p.url,
            "canonical_topic": p.canonical_topic,
            "tags": p.tags,
            "difficulty": p.difficulty,
            "acceptance_rate": p.acceptance_rate,
        }
        for p in catalog_problems
    ]

    ranked = recommendation_engine.rank_problems(
        candidate_problems=candidates,
        mastery_vector=mastery_vector,
        topic_elo_map=topic_elo_map,
        overall_elo=overall_elo,
        solved_problem_ids=solved_keys,
        mode=mode,
        target_topic=topic,
        limit=limit,
    )

    return {
        "user_id": current_user.id,
        "mode": mode,
        "filtered_topic": topic,
        "filtered_platform": platform,
        "user_overall_elo": overall_elo,
        "total_recommendations": len(ranked),
        "recommendations": ranked,
    }
