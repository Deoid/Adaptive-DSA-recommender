from typing import List, Dict, Any, Set, Optional
from backend.services.elo_matcher import elo_matcher
from backend.services.bkt_model import bkt_engine
from backend.services.canonical_topics import CANONICAL_TOPICS

class AdaptiveRecommendationEngine:
    """
    Ranks and surfaces DSA problems by fusing:
    1. Bayesian Knowledge Tracing (BKT) topic mastery probabilities.
    2. Elo-based Zone of Proximal Development (ZPD) difficulty matching.
    3. Solved problem deduplication across all 4 connected platforms.
    """

    def rank_problems(
        self,
        candidate_problems: List[Dict[str, Any]],
        mastery_vector: Dict[str, float], # topic -> P(L) in [0.0, 1.0]
        topic_elo_map: Dict[str, float],   # topic -> user elo
        overall_elo: float,
        solved_problem_ids: Set[str],
        mode: str = "balanced", # "balanced", "weakness_focus", "rating_push"
        target_topic: Optional[str] = None,
        limit: int = 15,
    ) -> List[Dict[str, Any]]:
        # Set weights based on recommendation focus mode
        if mode == "weakness_focus":
            w_zpd = 0.35
            w_bkt = 0.65
        elif mode == "rating_push":
            w_zpd = 0.75
            w_bkt = 0.25
        else: # balanced
            w_zpd = 0.55
            w_bkt = 0.45

        ranked_list = []

        for p in candidate_problems:
            pid = str(p.get("problem_id"))
            platform = str(p.get("platform", "")).lower()
            unique_key = f"{platform}:{pid}"

            # Filter out already solved problems across platforms
            if unique_key in solved_problem_ids or pid in solved_problem_ids:
                continue

            topic = p.get("canonical_topic", "General")
            if target_topic and topic != target_topic:
                continue

            difficulty = float(p.get("difficulty", 1200))
            user_topic_elo = topic_elo_map.get(topic, overall_elo)

            # 1. BKT Mastery Component
            # High growth potential exists where mastery is lower or developing
            mastery_prob = mastery_vector.get(topic, 0.15)
            # Growth room = 1 - P(L), clipped nicely
            growth_potential = max(0.05, 1.0 - mastery_prob)

            # 2. Elo ZPD Difficulty Fit Component
            zpd_fit = elo_matcher.calculate_zpd_fit(user_topic_elo, difficulty)
            expected_p = elo_matcher.expected_solve_probability(user_topic_elo, difficulty)

            # 3. Composite score fusion
            composite_score = (w_zpd * zpd_fit) + (w_bkt * growth_potential)

            # Rationale generation for explainability
            rating_delta = int(difficulty - user_topic_elo)
            delta_sign = "+" if rating_delta >= 0 else ""
            
            fit_analysis = elo_matcher.evaluate_problem_fit(user_topic_elo, difficulty)

            rationale = (
                f"Topic mastery is {int(mastery_prob * 100)}% ({topic}). "
                f"Problem difficulty {int(difficulty)} ({delta_sign}{rating_delta} Elo vs your skill) "
                f"gives an estimated {int(expected_p * 100)}% win rate in your {fit_analysis['difficulty_tier']}."
            )

            ranked_list.append({
                "id": p.get("id"),
                "problem_id": pid,
                "platform": platform,
                "title": p.get("title"),
                "url": p.get("url"),
                "canonical_topic": topic,
                "tags": p.get("tags"),
                "difficulty": int(difficulty),
                "acceptance_rate": p.get("acceptance_rate"),
                
                # Recommendation scoring metrics
                "composite_score": round(composite_score, 4),
                "zpd_score": zpd_fit,
                "mastery_probability": round(mastery_prob, 3),
                "expected_solve_probability": round(expected_p, 3),
                "rating_delta": rating_delta,
                "difficulty_tier": fit_analysis["difficulty_tier"],
                "fit_label": fit_analysis["fit_label"],
                "growth_potential": round(growth_potential, 3),
                "recommendation_rationale": rationale,
            })

        # Sort descending by composite score
        ranked_list.sort(key=lambda x: x["composite_score"], reverse=True)
        return ranked_list[:limit]

recommendation_engine = AdaptiveRecommendationEngine()
