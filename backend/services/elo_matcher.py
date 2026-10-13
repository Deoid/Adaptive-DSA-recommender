import math
from typing import Dict, Any

class EloDifficultyMatcher:
    """
    Elo Rating System and Difficulty Matching Layer for DSA problems.
    
    Compares solver skill against problem difficulty, computing:
    1. Expected win/solve probability E via logistic curve.
    2. Zone of Proximal Development (ZPD) fit score for optimal learning curve.
    3. Rating adjustment after submission outcomes.
    """

    K_FACTOR: float = 24.0
    OPTIMAL_RATING_DELTA: float = 75.0 # Target +75 rating points above current level for max growth
    SIGMA_BANDWIDTH: float = 180.0     # Gaussian spread around the optimal challenge point

    @staticmethod
    def expected_solve_probability(user_elo: float, problem_difficulty: float) -> float:
        """
        Calculates expected probability E that solver overcomes problem of rating `problem_difficulty`.
        E = 1 / (1 + 10 ^ ((R_problem - R_user) / 400))
        """
        exponent = (problem_difficulty - user_elo) / 400.0
        # Prevent math overflow
        exponent = max(-10.0, min(10.0, exponent))
        return 1.0 / (1.0 + math.pow(10.0, exponent))

    @classmethod
    def calculate_zpd_fit(
        cls, 
        user_elo: float, 
        problem_difficulty: float,
        target_delta: float = None
    ) -> float:
        """
        Zone of Proximal Development (ZPD) score [0.0, 1.0].
        Scores highest when problem difficulty is in the solver's optimal growth zone.
        """
        delta = target_delta if target_delta is not None else cls.OPTIMAL_RATING_DELTA
        ideal_problem_rating = user_elo + delta
        diff = problem_difficulty - ideal_problem_rating
        
        # Gaussian curve centered at ideal challenge difficulty
        zpd_score = math.exp(- (diff ** 2) / (2.0 * (cls.SIGMA_BANDWIDTH ** 2)))
        return round(zpd_score, 4)

    @classmethod
    def update_user_elo(
        cls, 
        current_elo: float, 
        problem_difficulty: float, 
        is_accepted: bool
    ) -> float:
        """
        Updates solver's rating using standard Elo formula after problem verdict.
        R_new = R_old + K * (Actual - Expected)
        """
        expected = cls.expected_solve_probability(current_elo, problem_difficulty)
        actual = 1.0 if is_accepted else 0.0
        new_elo = current_elo + cls.K_FACTOR * (actual - expected)
        # Keep rating within sensible bounds [600, 3600]
        return round(max(600.0, min(3600.0, new_elo)), 1)

    @classmethod
    def evaluate_problem_fit(
        cls,
        user_elo: float,
        problem_difficulty: float
    ) -> Dict[str, Any]:
        expected_prob = cls.expected_solve_probability(user_elo, problem_difficulty)
        zpd_score = cls.calculate_zpd_fit(user_elo, problem_difficulty)
        rating_diff = problem_difficulty - user_elo

        if rating_diff > 300:
            difficulty_tier = "Extremely Challenging"
            fit_label = "Stretch Goal (High Frustration Risk)"
        elif rating_diff >= 50:
            difficulty_tier = "Optimal Growth Zone"
            fit_label = "Sweet Spot (Maximum Skill Acquisition)"
        elif rating_diff >= -100:
            difficulty_tier = "Reinforcement"
            fit_label = "Confidence Builder (Skill Solidification)"
        else:
            difficulty_tier = "Below Skill Level"
            fit_label = "Speed Drill / Trivial"

        return {
            "expected_solve_prob": round(expected_prob, 3),
            "zpd_score": zpd_score,
            "rating_delta": int(rating_diff),
            "difficulty_tier": difficulty_tier,
            "fit_label": fit_label,
        }

elo_matcher = EloDifficultyMatcher()
