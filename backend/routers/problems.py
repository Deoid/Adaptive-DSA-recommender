from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_db
from backend.models.problem import ProblemCatalog
from backend.seed_data import seed_problems_catalog

router = APIRouter(prefix="/problems", tags=["Problems Catalog"])

@router.get("")
async def list_problems(
    topic: Optional[str] = Query(None),
    platform: Optional[str] = Query(None),
    min_difficulty: Optional[int] = Query(None),
    max_difficulty: Optional[int] = Query(None),
    limit: int = Query(25, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(ProblemCatalog)
    if topic:
        query = query.where(ProblemCatalog.canonical_topic == topic)
    if platform and platform.lower() != "all":
        query = query.where(ProblemCatalog.platform == platform.lower())
    if min_difficulty:
        query = query.where(ProblemCatalog.difficulty >= min_difficulty)
    if max_difficulty:
        query = query.where(ProblemCatalog.difficulty <= max_difficulty)

    query = query.limit(limit)
    res = await db.execute(query)
    problems = res.scalars().all()
    return problems

@router.post("/seed")
async def trigger_seed(db: AsyncSession = Depends(get_db)):
    await seed_problems_catalog(db)
    return {"status": "success", "message": "Catalog initialized"}
