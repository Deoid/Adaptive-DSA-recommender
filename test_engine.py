import asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.database import init_db

async def run_tests():
    print(">>> Starting Comprehensive Verification Test for Adaptive DSA Engine...")
    await init_db()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Test API health
        res = await client.get("/api/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        print(" [OK] API health endpoint status:", res.json()["status"])

        # 2. Test Registration
        register_payload = {
            "username": "tourist_coder",
            "email": "tourist@example.com",
            "password": "Password123!",
            "codeforces_handle": "tourist",
            "leetcode_handle": "neal_wu",
            "codechef_handle": "gennady",
            "atcoder_handle": "tourist",
        }
        res = await client.post("/api/auth/register", json=register_payload)
        assert res.status_code in [200, 400], f"Registration failed: {res.text}"
        
        # 3. Test Login
        login_res = await client.post("/api/auth/login", json={
            "username_or_email": "tourist_coder",
            "password": "Password123!"
        })
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print(" [OK] Auth registered & logged in with JWT token")

        # 4. Test BKT simulate
        bkt_sim = await client.post("/api/bkt/simulate", json={
            "initial_p_l": 0.15,
            "verdicts": [True, True, False, True, True],
            "user_elo": 1400.0,
            "problem_difficulty": 1500.0
        })
        assert bkt_sim.status_code == 200, f"BKT simulate failed: {bkt_sim.text}"
        data = bkt_sim.json()
        print(f" [OK] BKT simulation passed. New P(L)={data['bkt_result']['mastery_probability']}, Status={data['bkt_result']['status']}")

        # 5. Test Submit Verdict (Single-step BKT + Elo update)
        verdict_res = await client.post("/api/bkt/submit-verdict", headers=headers, json={
            "topic": "Dynamic Programming",
            "problem_id": "455A",
            "problem_title": "Boredom",
            "platform": "codeforces",
            "difficulty": 1500,
            "is_accepted": True
        })
        assert verdict_res.status_code == 200, f"Submit verdict failed: {verdict_res.text}"
        v_data = verdict_res.json()
        print(f" [OK] Live submission processed: DP mastery={v_data['new_mastery_probability']}, Topic Elo={v_data['new_topic_elo']}")

        # 6. Test Mastery Vector endpoint
        mastery_res = await client.get("/api/bkt/mastery", headers=headers)
        assert mastery_res.status_code == 200, f"Mastery get failed: {mastery_res.text}"
        m_data = mastery_res.json()
        print(f" [OK] Mastery vector retrieved: {len(m_data['topics'])} canonical topics")

        # 7. Test Recommendations ranking endpoint
        rec_res = await client.get("/api/recommendations?mode=balanced&limit=5", headers=headers)
        assert rec_res.status_code == 200, f"Recommendations failed: {rec_res.text}"
        recs = rec_res.json()
        print(f" [OK] Surfaced {len(recs['recommendations'])} adaptive recommendations:")
        for r in recs["recommendations"][:3]:
            print(f"      * [{r['platform'].upper()}] {r['title']} (Rating: {r['difficulty']}, Topic: {r['canonical_topic']})")
            print(f"        Composite Score: {r['composite_score']} | ZPD: {r['zpd_score']} | P(Mastery): {r['mastery_probability']}")
            print(f"        Rationale: {r['recommendation_rationale']}")

        # 8. Test Platform Sync & Topic Breakdown
        sync_res = await client.get("/api/platforms/stats", headers=headers)
        assert sync_res.status_code == 200, f"Stats failed: {sync_res.text}"
        s_data = sync_res.json()
        print(f" [OK] Platform stats & topic breakdown retrieved successfully:")
        print(f"      Combined Total Solved: {s_data['problems_solved']['combined_total']}")
        print(f"      Ratings: CF={s_data['ratings']['codeforces']['rating']}, LC={s_data['ratings']['leetcode']['rating']}, CC={s_data['ratings']['codechef']['rating']}, AC={s_data['ratings']['atcoder']['rating']}")
        print(f"      Overall Unified Elo: {s_data['ratings']['overall_unified_elo']}")

    print("\n>>> ALL BACKEND CORE CAPABILITIES VALIDATED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    asyncio.run(run_tests())
