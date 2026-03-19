import sys
import os
from typing import TYPE_CHECKING, List

# ─── Fix Path Resolution (Ensures app modules can be found despite space in path) ───
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ─── TYPE_CHECKING Guard ──────────────────────────────────────────────────
if TYPE_CHECKING:
    def invoke_model(prompt: str, system_prompt: str = None) -> str: ... # type: ignore
else:
    from app.services.bedrock_client import invoke_model

PROMPT = "Explain polymorphism in one sentence."

def test_bedrock_invoke() -> None:
    print("\n" + "=" * 50)
    print(f"DEBUG: Running Bedrock test...")
    print(f"PROMPT : {PROMPT}")
    print("=" * 50)

    try:
        response = invoke_model(PROMPT)
        
        print(f"RESPONSE:\n{response}")
        print("=" * 50)

        # In modern version, errors are returned as a string starting with "Service temporarily unavailable"
        if "Service temporarily unavailable" in response:
            print("[FAIL] Test FAILED: Bedrock was unable to respond (Check AWS credentials/quotas)")
            sys.exit(1)
        
        if not response or not response.strip():
            print("[FAIL] Test FAILED: Empty response from model")
            sys.exit(1)

        print("[PASS] Test PASSED: Bedrock responded successfully!")
        
    except Exception as e:
        print(f"[FAIL] Test FAILED with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_bedrock_invoke()
