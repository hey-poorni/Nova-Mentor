import json
import logging
import re
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    # Only seen by the linter/IDE to resolve the import without path issues
    def invoke_model(prompt: str, system_prompt: Optional[str] = None) -> str: ...
else:
    # Used at runtime by the actual Python engine
    from .bedrock_client import invoke_model

logger = logging.getLogger(__name__)

# --- LAYER 1: RULE-BASED (MANDATORY) ---
# Mapping weak topics to pre-defined recommendations
TOPIC_MAP = {
    "sorting": [
        "basic sorting concepts",
        "bubble sort",
        "merge sort",
        "quick sort"
    ],
    "arrays": [
        "array basics",
        "array traversal",
        "prefix sum",
        "sliding window"
    ],
    "binary search": [
        "binary search basics",
        "lower bound",
        "upper bound",
        "search on answer"
    ],
    "linked list": [
        "singly linked list",
        "doubly linked list",
        "fast and slow pointers",
        "reverse a linked list"
    ],
    "recursion": [
        "base case understanding",
        "recursive tree",
        "memoization",
        "backtracking"
    ]
}

def recommend_rule_based(weak_topics: list) -> list:
    """
    Returns recommendations based on the pre-defined TOPIC_MAP.
    """
    recommendations = []
    
    for topic in weak_topics:
        t_lower = topic.lower()
        if t_lower in TOPIC_MAP:
            recommendations.extend(TOPIC_MAP[t_lower])
        else:
            recommendations.append(f"learn basics of {topic}")
            
    # Remove duplicates while preserving some order order (using dict keys)
    return list(dict.fromkeys(recommendations))


def _extract_list(text: str) -> List[str]:
    """Robustly extract a list string from text."""
    text = text.strip()

    # Try finding a markdown code block first
    match = re.search(r"```(?:json|python)?\s*(\[.*?\])\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        try:
            result = json.loads(match.group(1).replace("'", '"'))
            if isinstance(result, list):
                return [str(item) for item in result]
        except (json.JSONDecodeError, ValueError):
            pass

    # Try finding anything between brackets
    match = re.search(r"(\[.*\])", text, re.DOTALL)
    if match:
        try:
            result = json.loads(match.group(1).replace("'", '"'))
            if isinstance(result, list):
                return [str(item) for item in result]
        except (json.JSONDecodeError, ValueError):
            pass

    # Fallback: return empty list
    return []

# --- LAYER 2: AI-BASED (OPTIONAL) ---
def recommend_with_ai(weak_topics: list) -> list:
    """
    Uses AWS Bedrock to generate learning topic recommendations.
    """
    if not weak_topics:
        return []

    prompt = f"""You are a personalized learning assistant.

Based on the student's weak areas: {', '.join(weak_topics)}
Provide 5 highly relevant topics for their next study session.

Return ONLY a valid JSON list of strings.
Example: ["Binary Search Tree", "DFS", "Heaps"]
"""

    try:
        response_text: str = invoke_model(prompt)
        topics: List[str] = _extract_list(response_text)

        if topics:
            return [t for i, t in enumerate(topics) if i < 5]  # Limit to top 5

        return recommend_rule_based(weak_topics)

    except Exception as e:
        logger.error(f"AI recommendation failed: {e}. Falling back to rule-based.")
        return recommend_rule_based(weak_topics)



# --- FINAL FUNCTION ---
def recommend_topics(weak_topics: list, use_ai: bool = False) -> list:
    """
    Main entry point for the recommendation engine.
    Supports both rule-based (default) and AI-based (optional) logic.
    """
    if not weak_topics:
        return []
        
    if use_ai:
        return recommend_with_ai(weak_topics)
    else:
        return recommend_rule_based(weak_topics)


# --- TESTING ---
if __name__ == "__main__":
    # Mocking invoke_model for the local test block if needed, 
    # but here we just run it to see the structure.
    weak = ["sorting", "arrays"]

    print("--- Testing Recommendation Engine ---")
    print("Rule-based:", recommend_topics(weak))
    
    try:
        print("AI-based (Attempt):", recommend_topics(weak, use_ai=True))
    except Exception as e:
        print(f"AI-based failed (expected if keys not set): {e}")
