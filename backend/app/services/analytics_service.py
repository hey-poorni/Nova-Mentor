import logging
import threading
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

# --- Analytics Tracker Class (Simplest Linter-Proof Approach) ---
class AnalyticsTracker:
    def __init__(self):
        self._lock = threading.Lock()
        # history: 1 for correct, 0 for incorrect.
        self.history: List[int] = []

    def track_attempt(self, is_correct: bool):
        with self._lock:
            # Atomic append is always safe for linters to track
            self.history.append(1 if is_correct else 0)
            logger.info(f"Attempt tracked. Total: {len(self.history)}")

    def get_summary(self) -> Dict[str, Any]:
        with self._lock:
            # Use reliable built-ins to avoid linter inference bugs
            h = self.history
            total = len(h)
            correct = sum(h)
            incorrect = total - correct
            
            # Accuracy
            accuracy = 0.0
            if total > 0:
                raw_acc = (float(correct) * 100.0) / float(total)
                accuracy = float(int(raw_acc * 100 + 0.5) / 100.0)
            
            # Recent (last 5)
            r_limit = 5
            r_items: List[int] = []
            # Collecting last N without using the [:] operator
            for v in reversed(h):
                if len(r_items) >= r_limit:
                    break
                r_items.append(v)
            
            r_total = len(r_items)
            r_accuracy = 0.0
            if r_total > 0:
                raw_r = (float(sum(r_items)) * 100.0) / float(r_total)
                r_accuracy = float(int(raw_r * 100 + 0.5) / 100.0)


            return {
                "total_attempts": total,
                "correct_answers": correct,
                "incorrect_answers": incorrect,
                "accuracy": accuracy,
                "recent_accuracy_last_5": r_accuracy
            }

    def reset(self):
        with self._lock:
            self.history = []
            logger.info("Analytics reset successfully.")

# --- Singleton Instance ---
_tracker = AnalyticsTracker()

# --- Public API Wrappers ---
def track_attempt(is_correct: bool):
    _tracker.track_attempt(is_correct)

def calculate_accuracy() -> float:
    return _tracker.get_summary()["accuracy"]

def get_recent_accuracy(last_n: int = 5) -> float:
    return _tracker.get_summary()["recent_accuracy_last_5"]

def get_summary() -> dict:
    return _tracker.get_summary()

def reset_analytics():
    _tracker.reset()

# --- TESTING BLOCK ---
if __name__ == "__main__":
    track_attempt(True) 
    track_attempt(False)
    print("Summary:", get_summary())
    reset_analytics()
    print("After Reset:", get_summary())


