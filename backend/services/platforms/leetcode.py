import httpx
from typing import Dict, Any, List, Optional

class LeetCodeClient:
    GRAPHQL_URL = "https://leetcode.com/graphql"

    async def get_user_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """Queries LeetCode public GraphQL for solved problems, rating, and topic stats."""
        if not username:
            return None

        query = """
        query getUserProfile($username: String!) {
            matchedUser(username: $username) {
                username
                profile {
                    ranking
                    userAvatar
                }
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
                tagProblemCounts {
                    advanced {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    intermediate {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    fundamental {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                }
            }
            userContestRanking(username: $username) {
                rating
                globalRanking
                totalParticipants
                topPercentage
            }
        }
        """

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    self.GRAPHQL_URL,
                    json={"query": query, "variables": {"username": username}},
                    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
                )
                data = res.json()
                user = data.get("data", {}).get("matchedUser")
                if not user:
                    return None

                contest = data.get("data", {}).get("userContestRanking") or {}
                submit_stats = user.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
                
                total_solved = 0
                easy_solved = 0
                medium_solved = 0
                hard_solved = 0
                for item in submit_stats:
                    diff = item.get("difficulty", "").lower()
                    cnt = item.get("count", 0)
                    if diff == "all":
                        total_solved = cnt
                    elif diff == "easy":
                        easy_solved = cnt
                    elif diff == "medium":
                        medium_solved = cnt
                    elif diff == "hard":
                        hard_solved = cnt

                # Collect tag solved stats
                tag_counts = user.get("tagProblemCounts", {})
                topic_solved = {}
                for category in ["fundamental", "intermediate", "advanced"]:
                    for item in tag_counts.get(category, []):
                        name = item.get("tagName", "")
                        count = item.get("problemsSolved", 0)
                        if name and count:
                            topic_solved[name] = count

                contest_rating = int(contest.get("rating", 1500)) if contest.get("rating") else 1500

                return {
                    "username": username,
                    "rating": contest_rating,
                    "global_ranking": contest.get("globalRanking") or user.get("profile", {}).get("ranking", 0),
                    "total_solved": total_solved,
                    "easy_solved": easy_solved,
                    "medium_solved": medium_solved,
                    "hard_solved": hard_solved,
                    "topic_solved": topic_solved,
                    "avatar": user.get("profile", {}).get("userAvatar", ""),
                }
        except Exception as e:
            print(f"[LeetCodeClient] Error fetching user profile for {username}: {e}")
        return None

    async def get_recent_submissions(self, username: str) -> List[Dict[str, Any]]:
        """Queries recent accepted submissions on LeetCode."""
        if not username:
            return []
        query = """
        query getRecentAcSubmissions($username: String!) {
            recentAcSubmissionList(username: $username, limit: 20) {
                id
                title
                titleSlug
                timestamp
            }
        }
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    self.GRAPHQL_URL,
                    json={"query": query, "variables": {"username": username}},
                    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
                )
                data = res.json()
                items = data.get("data", {}).get("recentAcSubmissionList", [])
                return [
                    {
                        "id": str(item.get("id")),
                        "problem_id": item.get("titleSlug"),
                        "title": item.get("title"),
                        "platform": "leetcode",
                        "verdict": "AC",
                        "is_accepted": True,
                        "timestamp": item.get("timestamp"),
                    }
                    for item in items
                ]
        except Exception as e:
            print(f"[LeetCodeClient] Error fetching recent submissions for {username}: {e}")
        return []

leetcode_client = LeetCodeClient()
