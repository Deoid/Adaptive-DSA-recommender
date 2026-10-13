import asyncio
from datetime import datetime
from typing import Dict, Any, List, Set
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.models.user import User
from backend.models.submission import UserSubmission
from backend.models.bkt_state import TopicMasteryState
from backend.services.platforms.codeforces import codeforces_client
from backend.services.platforms.leetcode import leetcode_client
from backend.services.platforms.codechef import codechef_client
from backend.services.platforms.atcoder import atcoder_client
from backend.services.canonical_topics import CANONICAL_TOPICS, normalize_tags_to_canonical, map_tag_to_canonical
from backend.services.bkt_model import bkt_engine
from backend.services.elo_matcher import elo_matcher

class MultiPlatformAggregator:
    """
    Coordinates data synchronization across Codeforces, LeetCode, CodeChef, and AtCoder:
    - Normalizes ratings and solves counts
    - Categorizes problems solved per canonical DSA topic
    - Drives Bayesian Knowledge Tracing updates per topic
    """

    async def sync_user_data(self, user: User, db: AsyncSession) -> Dict[str, Any]:
        tasks = []
        
        # Parallel fetch from all connected platforms
        tasks.append(codeforces_client.get_user_info(user.codeforces_handle))
        tasks.append(codeforces_client.get_user_status_data(user.codeforces_handle))
        tasks.append(leetcode_client.get_user_profile(user.leetcode_handle))
        tasks.append(leetcode_client.get_recent_submissions(user.leetcode_handle))
        tasks.append(codechef_client.get_user_profile(user.codechef_handle))
        tasks.append(atcoder_client.get_user_profile(user.atcoder_handle))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        cf_info = results[0] if isinstance(results[0], dict) else None
        cf_status = results[1] if isinstance(results[1], dict) else {}
        cf_subs = cf_status.get("recent_submissions", [])
        cf_total_ac = cf_status.get("total_ac_solved", 0)
        
        lc_profile = results[2] if isinstance(results[2], dict) else None
        lc_subs = results[3] if isinstance(results[3], list) else []
        cc_profile = results[4] if isinstance(results[4], dict) else None
        at_profile = results[5] if isinstance(results[5], dict) else None

        # 1. Collect platform ratings
        cf_rating = cf_info.get("rating", 1200) if cf_info else 1200
        lc_rating = lc_profile.get("rating", 1500) if lc_profile else 1500
        cc_rating = cc_profile.get("rating", 1400) if cc_profile else 1400
        at_rating = at_profile.get("rating", 1000) if at_profile else 1000

        # Weighted combined Elo skill baseline
        active_ratings = []
        if user.codeforces_handle and cf_info:
            active_ratings.append(cf_rating)
        if user.leetcode_handle and lc_profile:
            active_ratings.append(lc_rating)
        if user.codechef_handle and cc_profile:
            active_ratings.append(cc_rating)
        if user.atcoder_handle and at_profile:
            active_ratings.append(at_rating + 300) # AtCoder ratings are harsher, normalize by +300

        overall_elo = round(sum(active_ratings) / len(active_ratings)) if active_ratings else user.user_overall_elo or 1300
        user.user_overall_elo = overall_elo

        # 2. Existing submissions deduplication
        existing_res = await db.execute(
            select(UserSubmission.problem_id, UserSubmission.platform).where(UserSubmission.user_id == user.id)
        )
        existing_keys = {f"{row[1]}:{row[0]}" for row in existing_res.fetchall()}

        new_submissions: List[UserSubmission] = []

        # Process Codeforces submissions
        for sub in cf_subs:
            key = f"codeforces:{sub['problem_id']}"
            if key not in existing_keys:
                canonical = normalize_tags_to_canonical(sub.get("tags", []), "codeforces")
                new_sub = UserSubmission(
                    user_id=user.id,
                    platform="codeforces",
                    problem_id=sub["problem_id"],
                    problem_title=sub["title"],
                    canonical_topic=canonical,
                    platform_tags=",".join(sub.get("tags", [])),
                    verdict=sub["verdict"],
                    is_accepted=sub["is_accepted"],
                    difficulty=sub.get("rating", 1200),
                    submission_time=datetime.fromtimestamp(sub.get("timestamp", datetime.utcnow().timestamp())),
                )
                new_submissions.append(new_sub)
                existing_keys.add(key)

        # Process LeetCode submissions
        for sub in lc_subs:
            key = f"leetcode:{sub['problem_id']}"
            if key not in existing_keys:
                canonical = "Data Structures (Stack, Queue, Heap, DSU)"
                new_sub = UserSubmission(
                    user_id=user.id,
                    platform="leetcode",
                    problem_id=sub["problem_id"],
                    problem_title=sub["title"],
                    canonical_topic=canonical,
                    platform_tags="",
                    verdict=sub["verdict"],
                    is_accepted=sub["is_accepted"],
                    difficulty=1400,
                    submission_time=datetime.fromtimestamp(sub.get("timestamp", datetime.utcnow().timestamp())),
                )
                new_submissions.append(new_sub)
                existing_keys.add(key)

        if new_submissions:
            db.add_all(new_submissions)
            await db.commit()

        # 3. Query all user submissions to run sliding-window BKT per topic
        subs_res = await db.execute(
            select(UserSubmission)
            .where(UserSubmission.user_id == user.id)
            .order_by(UserSubmission.submission_time.asc())
        )
        all_user_subs = subs_res.scalars().all()

        # Group submissions by topic
        topic_subs_map: Dict[str, List[UserSubmission]] = {t: [] for t in CANONICAL_TOPICS}
        for s in all_user_subs:
            if s.canonical_topic in topic_subs_map:
                topic_subs_map[s.canonical_topic].append(s)

        # Calculate BKT mastery state and topic Elo per topic
        mastery_results: Dict[str, Dict[str, Any]] = {}
        for topic in CANONICAL_TOPICS:
            subs = topic_subs_map[topic]
            verdicts = [s.is_accepted for s in subs]
            
            # Run BKT with sliding window of 20
            bkt_res = bkt_engine.compute_from_submissions(verdicts, initial_prior=0.15)
            
            # Compute topic Elo starting from baseline
            current_topic_elo = float(overall_elo)
            for s in subs:
                current_topic_elo = elo_matcher.update_user_elo(
                    current_topic_elo, 
                    s.difficulty or current_topic_elo, 
                    s.is_accepted
                )

            # Persist or update TopicMasteryState
            state_res = await db.execute(
                select(TopicMasteryState).where(
                    TopicMasteryState.user_id == user.id,
                    TopicMasteryState.topic == topic
                )
            )
            state = state_res.scalar_one_or_none()
            if not state:
                state = TopicMasteryState(
                    user_id=user.id,
                    topic=topic,
                    mastery_probability=bkt_res["mastery_probability"],
                    prior_probability=0.15,
                    total_attempts=len(subs),
                    correct_attempts=sum(1 for s in subs if s.is_accepted),
                    recent_window_accuracy=bkt_res["window_accuracy"],
                    topic_elo=current_topic_elo,
                )
                db.add(state)
            else:
                state.mastery_probability = bkt_res["mastery_probability"]
                state.total_attempts = len(subs)
                state.correct_attempts = sum(1 for s in subs if s.is_accepted)
                state.recent_window_accuracy = bkt_res["window_accuracy"]
                state.topic_elo = current_topic_elo
                state.last_updated = datetime.utcnow()

            mastery_results[topic] = {
                "mastery_probability": bkt_res["mastery_probability"],
                "topic_elo": round(current_topic_elo, 1),
                "status": bkt_res["status"],
                "total_attempts": len(subs),
                "correct_attempts": sum(1 for s in subs if s.is_accepted),
                "window_accuracy": bkt_res["window_accuracy"],
            }

        await db.commit()

        # 4. Solved breakdown calculations across all 4 platforms
        cf_solved_count = cf_total_ac if user.codeforces_handle and cf_total_ac > 0 else len([s for s in all_user_subs if s.platform == "codeforces" and s.is_accepted])
        lc_solved_count = (lc_profile.get("total_solved", 0) if lc_profile else 0)
        cc_solved_count = (cc_profile.get("total_solved", 0) if cc_profile else 0)
        at_solved_count = (at_profile.get("accepted_count", 0) if at_profile else 0)
        
        combined_total_solved = cf_solved_count + lc_solved_count + cc_solved_count + at_solved_count

        # Topic solved breakdown:
        # Combine database verified ACs with LeetCode & Codeforces tag breakdowns
        topic_solved_breakdown: Dict[str, int] = {}
        total_db_acs = sum(sum(1 for s in topic_subs_map[t] if s.is_accepted) for t in CANONICAL_TOPICS)

        for topic in CANONICAL_TOPICS:
            db_ac_count = sum(1 for s in topic_subs_map[topic] if s.is_accepted)
            
            # Incorporate LeetCode tag counts mapped to this topic
            lc_extra = 0
            if lc_profile and "topic_solved" in lc_profile:
                for tag, count in lc_profile["topic_solved"].items():
                    if map_tag_to_canonical(tag, "leetcode") == topic:
                        lc_extra += count

            # Proportional Codeforces topic distribution if high AC count
            cf_extra = 0
            if cf_solved_count > len(all_user_subs) and total_db_acs > 0:
                topic_ratio = db_ac_count / total_db_acs
                cf_extra = int(cf_solved_count * topic_ratio)

            topic_solved_breakdown[topic] = db_ac_count + lc_extra + cf_extra

        return {
            "ratings": {
                "codeforces": {
                    "handle": user.codeforces_handle,
                    "rating": cf_rating,
                    "rank": cf_info.get("rank", "unrated") if cf_info else "unrated",
                    "maxRating": cf_info.get("maxRating", cf_rating) if cf_info else cf_rating,
                },
                "leetcode": {
                    "handle": user.leetcode_handle,
                    "rating": lc_rating,
                    "global_ranking": lc_profile.get("global_ranking", 0) if lc_profile else 0,
                    "easy": lc_profile.get("easy_solved", 0) if lc_profile else 0,
                    "medium": lc_profile.get("medium_solved", 0) if lc_profile else 0,
                    "hard": lc_profile.get("hard_solved", 0) if lc_profile else 0,
                },
                "codechef": {
                    "handle": user.codechef_handle,
                    "rating": cc_rating,
                    "stars": cc_profile.get("stars", "1★") if cc_profile else "1★",
                    "global_rank": cc_profile.get("global_rank", 0) if cc_profile else 0,
                },
                "atcoder": {
                    "handle": user.atcoder_handle,
                    "rating": at_rating,
                    "tier": at_profile.get("tier", "Gray") if at_profile else "Gray",
                    "highest_rating": at_profile.get("highest_rating", at_rating) if at_profile else at_rating,
                },
                "overall_unified_elo": overall_elo,
            },
            "problems_solved": {
                "combined_total": combined_total_solved,
                "platform_breakdown": {
                    "codeforces": cf_solved_count,
                    "leetcode": lc_solved_count,
                    "codechef": cc_solved_count,
                    "atcoder": at_solved_count,
                },
                "topic_breakdown": topic_solved_breakdown,
            },
            "bkt_mastery_vector": mastery_results,
        }

aggregator = MultiPlatformAggregator()
