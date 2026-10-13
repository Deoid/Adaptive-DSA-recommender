from typing import List, Dict, Any, Optional

class BayesianKnowledgeTracing:
    """
    Standard Bayesian Knowledge Tracing (BKT) Model with sliding window processing.
    
    Parameters:
    - L0: Prior probability of knowing the skill initially.
    - T:  Probability of transitioning from unlearned to learned state after an attempt.
    - G:  Probability of a 'Guess' (getting Accepted without knowing the skill).
    - S:  Probability of a 'Slip' (getting Wrong-Answer despite knowing the skill).
    - window_size: Sliding window of recent attempts (default: 20 submissions).
    """

    DEFAULT_L0 = 0.15
    DEFAULT_TRANSIT = 0.10
    DEFAULT_GUESS = 0.15
    DEFAULT_SLIP = 0.08
    DEFAULT_WINDOW_SIZE = 20

    def __init__(
        self,
        p_l0: float = DEFAULT_L0,
        p_transit: float = DEFAULT_TRANSIT,
        p_guess: float = DEFAULT_GUESS,
        p_slip: float = DEFAULT_SLIP,
        window_size: int = DEFAULT_WINDOW_SIZE,
    ):
        self.p_l0 = p_l0
        self.p_transit = p_transit
        self.p_guess = p_guess
        self.p_slip = p_slip
        self.window_size = window_size

    def step_update(self, prior_p_l: float, is_correct: bool) -> float:
        """
        Calculates posterior probability P(L_k) after an observation (Accepted / Wrong-Answer).
        """
        # Clamp prior to prevent numerical degeneracy [0.001, 0.999]
        p_l = max(0.001, min(0.999, prior_p_l))

        # 1. Posterior calculation P(L_{k-1} | Outcome)
        if is_correct:
            # P(L | Correct) = P(L) * (1 - S) / [ P(L) * (1 - S) + (1 - P(L)) * G ]
            num = p_l * (1.0 - self.p_slip)
            denom = num + (1.0 - p_l) * self.p_guess
        else:
            # P(L | Incorrect) = P(L) * S / [ P(L) * S + (1 - P(L)) * (1 - G) ]
            num = p_l * self.p_slip
            denom = num + (1.0 - p_l) * (1.0 - self.p_guess)

        if denom <= 0:
            p_posterior = p_l
        else:
            p_posterior = num / denom

        # 2. Transition step: P(L_k) = P(L | Outcome) + (1 - P(L | Outcome)) * P(Transit)
        p_updated = p_posterior + (1.0 - p_posterior) * self.p_transit

        return max(0.01, min(0.99, p_updated))

    def compute_from_submissions(
        self,
        submissions_verdicts: List[bool],
        initial_prior: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Runs BKT over a sequence of verdicts (chronological order, oldest to newest),
        limiting computation to the last `window_size` (20) submissions per topic.
        """
        if initial_prior is None:
            initial_prior = self.p_l0

        # Enforce sliding window of last N submissions
        window = submissions_verdicts[-self.window_size:] if len(submissions_verdicts) > self.window_size else submissions_verdicts

        current_p_l = initial_prior
        history = [current_p_l]

        for is_correct in window:
            current_p_l = self.step_update(current_p_l, is_correct)
            history.append(current_p_l)

        total_in_window = len(window)
        correct_in_window = sum(1 for v in window if v)
        window_accuracy = (correct_in_window / total_in_window) if total_in_window > 0 else 0.0

        # Mastery categorization
        if current_p_l >= 0.80:
            status = "Mastered"
        elif current_p_l >= 0.60:
            status = "Competent"
        elif current_p_l >= 0.35:
            status = "Developing"
        else:
            status = "Novice"

        return {
            "mastery_probability": round(current_p_l, 4),
            "window_size": self.window_size,
            "submissions_analyzed": total_in_window,
            "window_accuracy": round(window_accuracy, 3),
            "history": [round(h, 4) for h in history],
            "status": status,
        }

bkt_engine = BayesianKnowledgeTracing()
