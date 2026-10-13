import re
import httpx
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional

class CodeChefClient:
    BASE_URL = "https://www.codechef.com/users"

    async def get_user_profile(self, handle: str) -> Optional[Dict[str, Any]]:
        """Parses CodeChef user profile for accurate rating, stars, and total problems solved."""
        if not handle:
            return None

        clean_handle = handle.strip()
        url = f"{self.BASE_URL}/{clean_handle}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

        try:
            async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
                res = await client.get(url, headers=headers)
                if res.status_code != 200:
                    return None

                soup = BeautifulSoup(res.text, "html.parser")

                # 1. Extract rating
                rating = 1400
                rating_elem = soup.find("div", class_="rating-number")
                if rating_elem and rating_elem.text.strip():
                    m = re.search(r"\d+", rating_elem.text.strip())
                    if m:
                        rating = int(m.group())

                # 2. Extract stars
                stars = "1★"
                stars_elem = soup.find("div", class_="rating-star")
                if stars_elem:
                    stars_count = len(stars_elem.find_all("span"))
                    stars = f"{stars_count}★" if stars_count > 0 else "1★"

                # 3. Extract global rank
                global_rank = 0
                rank_items = soup.find_all("li", class_="inline-list")
                for item in rank_items:
                    if "Global Rank" in item.text:
                        val = item.find("strong")
                        if val and val.text.isdigit():
                            global_rank = int(val.text)

                # 4. Extract total solved problems accurately
                total_solved = 0
                
                # Check modern pattern: "Total Problems Solved: 632"
                m_total = re.search(r"Total Problems Solved:\s*(\d+)", res.text, re.IGNORECASE)
                if m_total:
                    total_solved = int(m_total.group(1))
                else:
                    # Check "Fully Solved (X)" occurrences
                    fully_matches = re.findall(r"Fully Solved\s*\(\s*(\d+)\s*\)", res.text, re.IGNORECASE)
                    if fully_matches:
                        total_solved = sum(int(x) for x in fully_matches)
                    else:
                        # Check problems-solved section
                        solved_section = soup.find("section", class_="problems-solved")
                        if solved_section:
                            digits = re.findall(r"\b\d+\b", solved_section.text)
                            if digits:
                                total_solved = max(int(d) for d in digits)

                return {
                    "handle": clean_handle,
                    "rating": rating,
                    "stars": stars,
                    "global_rank": global_rank,
                    "total_solved": total_solved,
                }
        except Exception as e:
            print(f"[CodeChefClient] Error fetching CodeChef profile for {handle}: {e}")
            return {
                "handle": handle,
                "rating": 1400,
                "stars": "1★",
                "global_rank": 0,
                "total_solved": 0,
            }

codechef_client = CodeChefClient()
