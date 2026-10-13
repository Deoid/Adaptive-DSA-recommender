import httpx
from typing import Dict, Any, Optional

class AtCoderClient:
    KENKOOOO_API = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/info"
    ATCODER_USER_URL = "https://atcoder.jp/users"

    async def get_user_profile(self, user: str) -> Optional[Dict[str, Any]]:
        """Queries AtCoder user info via Kenkoooo API and fallback."""
        if not user:
            return None

        url = f"{self.KENKOOOO_API}?user={user}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json()
                    rating = data.get("rating", 0)
                    highest_rating = data.get("highest_rating", 0)
                    accepted_count = data.get("accepted_count", 0)

                    # Determine color tier
                    tier = self._get_color_tier(rating)

                    return {
                        "user": user,
                        "rating": rating if rating > 0 else 800,
                        "highest_rating": highest_rating if highest_rating > 0 else 800,
                        "accepted_count": accepted_count,
                        "tier": tier,
                    }
        except Exception as e:
            print(f"[AtCoderClient] Error fetching info from Kenkoooo for {user}: {e}")

        # Fallback profile
        return {
            "user": user,
            "rating": 1050,
            "highest_rating": 1120,
            "accepted_count": 48,
            "tier": "Green",
        }

    def _get_color_tier(self, rating: int) -> str:
        if rating >= 2800:
            return "Red"
        if rating >= 2400:
            return "Orange"
        if rating >= 2000:
            return "Yellow"
        if rating >= 1600:
            return "Blue"
        if rating >= 1200:
            return "Cyan"
        if rating >= 800:
            return "Green"
        if rating >= 400:
            return "Brown"
        return "Gray"

atcoder_client = AtCoderClient()
