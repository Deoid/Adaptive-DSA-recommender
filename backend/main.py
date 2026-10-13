from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import engine, init_db
from backend.routers import (
    auth_router,
    platforms_router,
    bkt_router,
    recommendations_router,
    problems_router,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables and seed catalog
    await init_db()

    yield

    # Shutdown
    await engine.dispose()

    yield

    # Shutdown
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Adaptive DSA Recommendation Engine powered by Bayesian Knowledge Tracing & Elo Rating Systems",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount API routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(platforms_router, prefix=settings.API_V1_STR)
app.include_router(bkt_router, prefix=settings.API_V1_STR)
app.include_router(recommendations_router, prefix=settings.API_V1_STR)
app.include_router(problems_router, prefix=settings.API_V1_STR)

@app.get("/api/health")
async def health():
    return {
        "engine": settings.PROJECT_NAME,
        "status": "online",
        "documentation": "/docs",
        "features": [
            "4 Platform Sync (Codeforces, LeetCode, CodeChef, AtCoder)",
            "Sliding-window Bayesian Knowledge Tracing (BKT) per DSA topic",
            "Elo-based Zone of Proximal Development (ZPD) difficulty matcher",
            "Personalized adaptive problem recommendation ranking",
        ]
    }

# Mount frontend build if available
dist_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(dist_dir):
    app.mount("/", StaticFiles(directory=dist_dir, html=True), name="static")
else:
    @app.get("/")
    async def root():
        return await health()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
