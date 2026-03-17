import json
import logging
from app.services.bedrock_client import invoke_model

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


def _extract_json(raw: str) -> dict:
    """
    Extract JSON from Bedrock response.
    Handles cases where the model wraps JSON in markdown code blocks.
    """
    # Strip markdown code fences if present
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first and last lines (``` or ```json)
        cleaned = "\n".join(lines[1:-1]).strip()

    return json.loads(cleaned)


def analyze_response(question: str, answer: str) -> dict:
    """
    Analyze a student's answer to a given question using AWS Bedrock.

    Args:
        question: The original question asked.
        answer: The student's answer.

    Returns:
        dict with keys: correctness, score, feedback

    Raises:
        ValueError: If Bedrock response cannot be parsed as JSON.
        RuntimeError: If Bedrock invocation fails entirely.
    """
    logger.info(f"Analyzing student response for question: {question[:60]}...")

    prompt = _build_analyzer_prompt(question, answer)
    raw_response = invoke_model(prompt)

    logger.info(f"Raw Bedrock response: {raw_response[:200]}")

    try:
        result = _extract_json(raw_response)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Bedrock JSON response: {e}")
        logger.error(f"Raw response was: {raw_response}")
        raise ValueError(
            f"Bedrock returned non-JSON response. Raw: {raw_response[:300]}"
        )

    # Validate required keys
    required_keys = {"correctness", "score", "feedback"}
    missing = required_keys - result.keys()
    if missing:
        raise ValueError(f"Response JSON missing required keys: {missing}")

    # Normalize correctness value
    correctness = result["correctness"].lower().strip()
    if correctness not in ("correct", "partial", "incorrect"):
        correctness = "incorrect"
    result["correctness"] = correctness

    # Clamp score to 0–100
    result["score"] = max(0, min(100, int(result["score"])))

    logger.info(f"Analysis result: {result}")
    return result
