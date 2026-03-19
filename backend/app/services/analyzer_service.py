import json
import logging
import re
from typing import Dict, Any

logger = logging.getLogger(__name__)



def _build_analyzer_prompt(question: str, answer: str) -> str:
    """Build the evaluation prompt for Bedrock."""
    return f"""Evaluate the student's answer.

Question: {question}
Student Answer: {answer}

Classify:
- correctness: must be exactly one of "correct", "partial", or "incorrect"
- score: integer from 0 to 100
- feedback: a short explanation of why

Return ONLY valid JSON in this exact format, no extra text:
{{
  "correctness": "correct | partial | incorrect",
  "score": 0-100,
  "feedback": "explanation"
}}"""


def _extract_json(text: str) -> Dict[str, Any]:
    """Robust extraction of JSON from LLM text, handling markdown blocks."""
    text = text.strip()
    
    # Try find markdown block
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        try: 
            return json.loads(match.group(1))
        except (json.JSONDecodeError, ValueError): 
            pass

    # Try find anything between { }
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        try: 
            return json.loads(match.group(1))
        except (json.JSONDecodeError, ValueError): 
            pass

    # Fallback to direct parse
    return json.loads(text)


from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    # These are only seen by the linter/IDE to clear red lines
    class HTTPException(Exception): 
        def __init__(self, status_code: int, detail: Any = None): ...
    def invoke_model(prompt: str, system_prompt: Any = None) -> str: ...
    def track_attempt(is_correct: bool) -> None: ...
else:
    # These are used at runtime by the actual Python engine
    from fastapi import HTTPException
    from .bedrock_client import invoke_model
    from .analytics_service import track_attempt

def analyze_response(question: str, answer: str) -> dict:
    """
    Analyze a student's answer to a given question using AWS Bedrock.
    """
    prompt = _build_analyzer_prompt(question, answer)
    
    try:
        raw_response = invoke_model(prompt)
    except Exception as e:
        logger.error(f"Bedrock invocation failed: {e}")
        raise HTTPException(status_code=503, detail="AI Service unavailable.")
    
    logger.debug(f"Raw Bedrock response: {raw_response}")

    try:
        result = _extract_json(raw_response)
    except Exception as e:
        logger.error(f"Failed to parse Bedrock response: {e}")


        # Return a safe fallback rather than crashing
        return {
            "correctness": "incorrect",
            "score": 0,
            "feedback": "System failed to evaluate answer. Please try again."
        }

    # Validate and Normalize
    correctness = str(result.get("correctness", "incorrect")).lower().strip()
    if correctness not in ("correct", "partial", "incorrect"):
        correctness = "incorrect"
    
    score = 0
    try:
        score = int(result.get("score", 0))
    except (ValueError, TypeError):
        score = 0

    # --- Integrated Analytics Tracking ---
    # Record the attempt in the global analytics service
    track_attempt(is_correct=(correctness == "correct"))


    final_result = {
        "correctness": correctness,
        "score": max(0, min(100, score)),
        "feedback": str(result.get("feedback", "No feedback available."))
    }

    logger.info(f"Analysis result tracked: {final_result['correctness']}")
    return final_result


