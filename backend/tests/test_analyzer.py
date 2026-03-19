# Test: analyzer_service.py
# Run: python backend/tests/test_analyzer.py

import sys
import os
from typing import TYPE_CHECKING, Any, Dict, List

# ─── Fix Path Resolution (Ensures app modules can be found despite space in path) ───
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ─── TYPE_CHECKING Guard ──────────────────────────────────────────────────
if TYPE_CHECKING:
    # Stubs for the IDE/linter to resolve types despite the "Projects E" path spaces
    def analyze_response(question: str, answer: str) -> Dict[str, Any]: ...
else:
    # Real runtime imports — uses the standard absolute path registered above
    from app.services.analyzer_service import analyze_response

# Sample test cases
TEST_CASES: List[Dict[str, str]] = [
    {
        "question": "What is sorting in computer science?",
        "answer": "Sorting is the process of arranging elements in a specific order, like ascending or descending.",
        "label": "CORRECT answer"
    },
    {
        "question": "What is sorting in computer science?",
        "answer": "Sorting is about putting things in order, but I am not sure exactly how it works in code.",
        "label": "PARTIAL answer"
    },
    {
        "question": "What is sorting in computer science?",
        "answer": "Sorting is when you delete duplicate items from a list.",
        "label": "INCORRECT answer"
    },
]

def run_tests() -> None:
    for case in TEST_CASES:
        print("\n" + "-" * 50)
        print(f"TEST: {case['label']}")
        print(f"Question: {case['question']}")
        print(f"Answer  : {case['answer']}")
        try:
            result = analyze_response(case["question"], case["answer"])
            print(f"Result  :")
            print(f"  correctness : {result['correctness']}")
            print(f"  score       : {result['score']}")
            print(f"  feedback    : {result['feedback']}")
        except Exception as e:
            print(f"[ERROR] {e}")

    print("\n" + "-" * 50)

if __name__ == "__main__":
    run_tests()
