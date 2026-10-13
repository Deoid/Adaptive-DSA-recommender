from backend.routers.auth import router as auth_router
from backend.routers.platforms import router as platforms_router
from backend.routers.bkt import router as bkt_router
from backend.routers.recommendations import router as recommendations_router
from backend.routers.problems import router as problems_router

__all__ = [
    "auth_router",
    "platforms_router",
    "bkt_router",
    "recommendations_router",
    "problems_router",
]
