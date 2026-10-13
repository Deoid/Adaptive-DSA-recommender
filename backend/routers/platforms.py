from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.user import User
from backend.auth.dependencies import get_current_user
from backend.services.platforms.aggregator import aggregator

router = APIRouter(prefix="/platforms", tags=["Platforms"])

@router.post("/sync")
async def sync_platform_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Synchronizes user's performance and submissions across all connected platforms
    (Codeforces, LeetCode, CodeChef, AtCoder), runs BKT sliding window, and updates mastery.
    """
    try:
        data = await aggregator.sync_user_data(current_user, db)
        return {
            "status": "success",
            "message": "All platform metrics and Bayesian mastery states synced successfully.",
            "data": data,
        }
    except Exception as e:
        print(f"[PlatformSync Error] {e}")
        raise HTTPException(status_code=500, detail=f"Failed to sync platform metrics: {str(e)}")

@router.get("/stats")
async def get_platform_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns latest stored metrics: platform ratings, total problems solved combined,
    and category-wise problem breakdown.
    """
    data = await aggregator.sync_user_data(current_user, db)
    return data
