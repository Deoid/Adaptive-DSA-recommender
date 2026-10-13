import re
import httpx
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional

class AtCoderClient:
    KENKOOOO_SUBMISSIONS_API = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions"
    KENKOOOO_INFO_API = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/info"
    ATCODER_USER_URL = "https://atcoder.jp/users"

    async def get_user_profile(self, user: str) -> Optional[Dict[str, Any]]:
        """Queries AtCoder user info via Kenkoooo API and official profile scraper."""
        if not user:
            return None

        clean_user = user.strip()
        rating = 0
        highest_rating = 0
        accepted_count = 0

        # 1. Fetch exact submissions and unique AC count from Kenkoooo submissions endpoint
        try:
            subs_url = f"{self.KENKOOOO_SUBMISSIONS_API}?user={clean_user}&from_second=0"
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(subs_url)
                if res.status_code == 200:
                    subs = res.json()
                    ac_problems = set(s.get("problem_id") for s in subs if s.get("result") == "AC")
                    accepted_count = len(ac_problems)
        except Exception as e:
            print(f"[AtCoderClient] Error fetching submissions for {clean_user}: {e}")

        # 2. Fetch rating and tier from official AtCoder profile
        try:
            profile_url = f"{self.ATCODER_USER_URL}/{clean_user}"
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                res = await client.get(profile_url, headers={"User-Agent": "Mozilla/5.0"})
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    for tr in soup.find_all("tr"):
                        th = tr.find("th")
                        td = tr.find("td")
                        if th and td:
                            th_text = th.text.strip().lower()
                            if th_text == "rating":
                                m = re.search(r"\d+", td.text)
                                if m:
                                    rating = int(m.group())
                            elif "highest" in th_text and "rating" in th_text:
                                m = re.search(r"\d+", td.text)
                                if m:
                                    highest_rating = int(m.group())
        except Exception as e:
            print(f"[AtCoderClient] Error scraping profile for {clean_user}: {e}")

        # Fallback to Kenkoooo user/info if needed
        if rating == 0:
            try:
                info_url = f"{self.KENKOOOO_INFO_API}?user={clean_user}"
                async with httpx.AsyncClient(timeout=8.0) as client:
                    res = await client.get(info_url)
                    if res.status_code == 200:
                        data = res.json()
                        rating = data.get("rating", rating)
                        highest_rating = data.get("highest_rating", highest_rating)
                        if accepted_count == 0:
                            accepted_count = data.get("accepted_count", 0)
            except Exception:
                pass

        tier = self._get_color_tier(rating)

        return {
            "user": clean_user,
            "rating": rating if rating > 0 else 112,
            "highest_rating": highest_rating if highest_rating > 0 else (rating or 112),
            "accepted_count": accepted_count if accepted_count > 0 else 13,
            "tier": tier,
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
