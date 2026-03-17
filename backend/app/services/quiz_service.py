import json
import logging
from app.services.bedrock_client import invoke_model

logger = logging.getLogger(__name__)


def _build_quiz_prompt(topic: str) -> str:
    """Build the quiz generation prompt for Bedrock."""
    return f"""You are a quiz generator.

Generate ONE multiple-choice question on the topic: {topic}

Rules:
- 4 options only
- Only one correct answer
- Include explanation
- Keep difficulty: beginner/intermediate

Return STRICT JSON only, no extra text:
{{
  "question": "",
  "options": ["A. option1", "B. option2", "C. option3", "D. option4"],
  "answer": "A",
  "explanation": ""
}}

DO NOT return anything else."""


def _extract_json(raw: str) -> dict:
    """
    Safely extract JSON from Bedrock response.
    Handles markdown code fences if present.
    """
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1]).strip()
    return json.loads(cleaned)


def generate_quiz(topic: str) -> dict:
    """
    Generate one MCQ on a given topic using AWS Bedrock.

    Args:
        topic: The subject/topic to generate the question on.

    Returns:
        dict with keys: question, options, answer, explanation

    Raises:
        ValueError: If Bedrock response is not valid JSON or missing keys.
        RuntimeError: If Bedrock invocation fails.
    """
    logger.info(f"Generating quiz for topic: {topic}")

    prompt = _build_quiz_prompt(topic)
    raw_response = invoke_model(prompt)

    logger.info(f"Raw Bedrock quiz response: {raw_response[:300]}")

    try:
        result = _extract_json(raw_response)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse quiz JSON: {e}")
        raise ValueError(f"Bedrock returned non-JSON quiz response. Raw: {raw_response[:300]}")

    # Validate required keys
    required_keys = {"question", "options", "answer", "explanation"}
    missing = required_keys - result.keys()
    if missing:
        raise ValueError(f"Quiz JSON missing required keys: {missing}")

    # Validate options count
    if not isinstance(result["options"], list) or len(result["options"]) != 4:
        raise ValueError(f"Quiz options must be a list of exactly 4 items. Got: {result['options']}")

    logger.info(f"Quiz generated successfully for topic: {topic}")
    return result
