import asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app

async def test_intermediate():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register new student coder
        reg = await client.post("/api/auth/register", json={
            "username": "algo_learner_demo",
            "email": "learner_demo@example.com",
            "password": "Password123!",
            "codeforces_handle": None,
            "leetcode_handle": None,
            "codechef_handle": None,
            "atcoder_handle": None
        })
        token = reg.json().get("access_token")
        if not token:
            login = await client.post("/api/auth/login", json={
                "username_or_email": "algo_learner_demo",
                "password": "Password123!"
            })
            token = login.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        
        # Get recommendations
        rec = await client.get("/api/recommendations?mode=balanced&limit=3", headers=headers)
        print(">>> Intermediate Learner (Elo 1300) Recommendations:")
        for r in rec.json()["recommendations"]:
            print(f" - [{r['platform'].upper()}] {r['title']} (Diff: {r['difficulty']}, Delta: {r['rating_delta']})")
            print(f"   Why: {r['recommendation_rationale']}")

if __name__ == "__main__":
    asyncio.run(test_intermediate())
