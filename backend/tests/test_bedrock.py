"""
Test: AWS Bedrock client – invoke_model()

Run:
    cd "e:\Projects E\Novamentor\src\Nova-Mentor"
    python -m backend.tests.test_bedrock

Expected output:
    INFO:app.services.bedrock_client:[Bedrock] Invoking primary model: amazon.nova-micro-v1:0
    INFO:app.services.bedrock_client:[Bedrock] Primary model responded successfully.
    ─────────────────────────────────────
    Prompt   : Hello AI
    Response : <AI response text>
    ─────────────────────────────────────
"""

import sys
import os

# ── Make sure backend/ is on the path so `app.*` imports work ────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.services.bedrock_client import invoke_model

PROMPT = "Hello AI"

def test_bedrock_invoke():
    print("\n─────────────────────────────────────")
    print(f"Prompt   : {PROMPT}")

    try:
        response = invoke_model(PROMPT)
        print(f"Response : {response}")
        print("─────────────────────────────────────\n")
        assert isinstance(response, str), "Response must be a string"
        assert len(response) > 0, "Response must not be empty"
        print("✅ Test PASSED")
    except RuntimeError as e:
        print(f"\n❌ Test FAILED – {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_bedrock_invoke()
