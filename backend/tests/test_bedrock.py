# Test: AWS Bedrock client - invoke_model()
# Run   : python backend/tests/test_bedrock.py
# Expect: Primary model responds with text, prints PASSED

import sys
import os

# ── Add backend/ to path so `app.*` imports work
# __file__ = Nova-Mentor/backend/tests/test_bedrock.py
# We go up one level to backend/ so `import app.services...` resolves
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.bedrock_client import invoke_model

PROMPT = "Hello AI"

def test_bedrock_invoke():
    print("\n" + "-" * 45)
    print(f"Prompt   : {PROMPT}")

    try:
        response = invoke_model(PROMPT)
        print(f"Response : {response}")
        print("-" * 45 + "\n")
        assert isinstance(response, str), "Response must be a string"
        assert len(response) > 0, "Response must not be empty"
        print("[PASS] Test PASSED - Bedrock responded successfully")
    except RuntimeError as e:
        print(f"\n[FAIL] Test FAILED - {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_bedrock_invoke()
