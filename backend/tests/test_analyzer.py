# Test: analyzer_service.py
# Run: python backend/tests/test_analyzer.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.analyzer_service import analyze_response

# Sample test cases
TEST_CASES = [
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

def run_tests():
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
