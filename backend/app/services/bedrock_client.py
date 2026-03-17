import boto3
import json
import logging
from app.core.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

# ─── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Model IDs ───────────────────────────────────────────────────────────────
PRIMARY_MODEL   = "amazon.nova-micro-v1:0"
FALLBACK_MODEL  = "nvidia.nemotron-nano-12b-v2"


# ─── Client Factory ──────────────────────────────────────────────────────────
def get_bedrock_client():
    """Return a boto3 bedrock-runtime client using credentials from .env."""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


# ─── Request Body Builders ───────────────────────────────────────────────────
def _nova_body(prompt: str) -> bytes:
    """
    Amazon Nova Micro request body.
    Content must be a list of text blocks, not a plain string.
    """
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}],   # Nova requires content as array
            }
        ],
        "inferenceConfig": {
            "maxTokens": 512,
            "temperature": 0.7,
        },
    }
    return json.dumps(payload).encode("utf-8")


def _nemotron_body(prompt: str) -> bytes:
    """
    NVIDIA Nemotron request body (standard Amazon Bedrock messages format).
    """
    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7,
    }
    return json.dumps(payload).encode("utf-8")


# ─── Response Parsers ────────────────────────────────────────────────────────
def _parse_nova_response(response_body: dict) -> str:
    """Parse text from Amazon Nova Micro response."""
    return response_body["output"]["message"]["content"][0]["text"]


def _parse_nemotron_response(response_body: dict) -> str:
    """Parse text from NVIDIA Nemotron response."""
    return response_body["choices"][0]["message"]["content"]


# ─── Core invoke_model function ──────────────────────────────────────────────
def invoke_model(prompt: str) -> str:
    """
    Send a prompt to AWS Bedrock and return the text response.

    Primary model  : amazon.nova-micro-v1:0
    Fallback model : nvidia.nemotron-nano-12b-v2

    Args:
        prompt: The user's input string.

    Returns:
        str: The model's text response.

    Raises:
        RuntimeError: If both primary and fallback models fail.
    """
    client = get_bedrock_client()

    # ── Attempt 1: Primary (Nova Micro) ──────────────────────────────────────
    try:
        logger.info(f"[Bedrock] Invoking primary model: {PRIMARY_MODEL}")

        raw = client.invoke_model(
            modelId=PRIMARY_MODEL,
            contentType="application/json",
            accept="application/json",
            body=_nova_body(prompt),
        )

        response_body = json.loads(raw["body"].read().decode("utf-8"))
        text = _parse_nova_response(response_body)

        logger.info("[Bedrock] Primary model responded successfully.")
        return text

    except client.exceptions.ModelNotReadyException as e:
        logger.warning(f"[Bedrock] Primary model not ready: {e}. Trying fallback.")
    except client.exceptions.ThrottlingException as e:
        logger.warning(f"[Bedrock] Primary model throttled: {e}. Trying fallback.")
    except client.exceptions.AccessDeniedException as e:
        logger.warning(f"[Bedrock] Primary model access denied: {e}. Trying fallback.")
    except Exception as e:
        logger.warning(f"[Bedrock] Primary model failed: {type(e).__name__}: {e}. Trying fallback.")

    # ── Attempt 2: Fallback (Nemotron) ───────────────────────────────────────
    try:
        logger.info(f"[Bedrock] Invoking fallback model: {FALLBACK_MODEL}")

        raw = client.invoke_model(
            modelId=FALLBACK_MODEL,
            contentType="application/json",
            accept="application/json",
            body=_nemotron_body(prompt),
        )

        response_body = json.loads(raw["body"].read().decode("utf-8"))
        text = _parse_nemotron_response(response_body)

        logger.info("[Bedrock] Fallback model responded successfully.")
        return text

    except Exception as e:
        logger.error(f"[Bedrock] Fallback model also failed: {type(e).__name__}: {e}")
        raise RuntimeError(
            f"Both models failed.\n"
            f"  Primary  ({PRIMARY_MODEL}): check above logs.\n"
            f"  Fallback ({FALLBACK_MODEL}): {e}"
        )
