import json
import logging
import re
from typing import Dict, Any, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    # This block is only seen by the linter/IDE to clear red lines
    def invoke_model(prompt: str, system_prompt: Optional[str] = None) -> str: ...
else:
    # This is used at runtime by the actual Python engine
    from .bedrock_client import invoke_model


logger = logging.getLogger(__name__)

def _extract_json(text: str) -> Dict[str, Any]:
    """Helper to extract JSON from text, handling markdown blocks and extra noise."""
    text = text.strip()
    
    # 1. Try direct JSON parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Try to find JSON inside markdown blocks
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 3. Last ditch effort: find anything between curly braces
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
            
    raise ValueError("Could not find valid JSON in LLM response.")

def generate_quiz(topic: str) -> Dict[str, Any]:
    """
    Generates a single multiple-choice question on a given topic using AWS Bedrock.
    Ensures a consistent return structure.
    """
    prompt = f"""You are a content generator for an educational platform.

Generate ONE high-quality multiple-choice question on the topic: {topic}

Rules:
- exactly 4 options
- exactly one correct answer
- clear, educational explanation for the answer
- difficulty level: beginner to intermediate

FORMAT: Return ONLY a single JSON object.
{{
  "question": "string",
  "options": ["A", "B", "C", "D"],
  "answer": "the EXACT text of the correct option",
  "explanation": "string explaining why"
}}"""

    try:
        response_text = invoke_model(prompt)
        quiz_data = _extract_json(response_text)
        
        # Validation & Normalization
        required_keys = ["question", "options", "answer", "explanation"]
        for key in required_keys:
            if key not in quiz_data:
                raise ValueError(f"Missing required key '{key}' in quiz JSON.")

        if not isinstance(quiz_data["options"], list) or len(quiz_data["options"]) != 4:
            raise ValueError("LLM returned incorrect number of options.")

        return quiz_data

    except Exception as e:
        logger.error(f"Quiz generation failed: {e}")
        # Return a graceful fallback question if something goes wrong
        return {
            "question": f"Could you explain your current understanding of {topic}?",
            "options": ["Needs more research", "Beginning to learn", "Some knowledge", "Expert"],
            "answer": "Some knowledge",
            "explanation": "This is a placeholder question because we had trouble reaching the AI service."
        }

