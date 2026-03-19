import json
import logging
import time
import threading
from typing import Optional, Dict, Any, TYPE_CHECKING, List

# ─── TYPE_CHECKING Guard (Fixes Path-Space Resolution Issues) ─────────────
if TYPE_CHECKING:
    # Minimal stubs to clear "red lines" caused by the space in project path
    class Config:
        def __init__(self, **kwargs: Any) -> None: ...
        
    class _Boto3Client:
        def invoke_model(self, **kwargs: Any) -> Dict[str, Any]: ...

    class _Boto3Module:
        def client(self, service_name: str, **kwargs: Any) -> _Boto3Client: ...

    # Explicitly define instances so the linter sees them as bound
    boto3: _Boto3Module = _Boto3Module() # type: ignore
    
    # Constant stubs for app.core.config
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_DEFAULT_REGION: str = ""
    PRIMARY_MODEL: str = ""
    FALLBACK_MODEL: str = ""
else:
    # Real runtime imports — kept in 'else' to avoid absolute path resolution errors
    import boto3
    from botocore.config import Config
    from ..core.config import (
        AWS_ACCESS_KEY_ID, 
        AWS_SECRET_ACCESS_KEY, 
        AWS_DEFAULT_REGION,
        PRIMARY_MODEL,
        FALLBACK_MODEL
    )

logger = logging.getLogger(__name__)

# ─── Boto3 Configuration ──────────────────────────────────────────────────
BOTO_CONFIG = Config(
    connect_timeout=10,
    read_timeout=35,
    retries={'max_attempts': 2}
)

# ─── Client Factory (Singleton) ──────────────────────────────────────────────
_client_instance: Any = None 
_client_lock = threading.Lock()

def get_bedrock_client():
    """Return a reused boto3 bedrock-runtime client with thread-safety."""
    global _client_instance
    if _client_instance is None:
        with _client_lock:
            if _client_instance is None:
                logger.info("[Bedrock] Creating new AWS Bedrock Runtime client...")
                try:
                    # Explicitly use boto3.client as defined in stubs/real module
                    instance = boto3.client(
                        service_name="bedrock-runtime",
                        region_name=AWS_DEFAULT_REGION or "us-east-1",
                        aws_access_key_id=AWS_ACCESS_KEY_ID if AWS_ACCESS_KEY_ID else None,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY if AWS_SECRET_ACCESS_KEY else None,
                        config=BOTO_CONFIG
                    )
                    _client_instance = instance
                except Exception as e:
                    logger.error(f"[Bedrock] Client creation failed: {e}")
                    raise
    return _client_instance


# ─── Request Body Builders ───────────────────────────────────────────────────
def _nova_body(prompt: str, system_prompt: Optional[str] = None) -> bytes:
    """Concise request format for Amazon Nova."""
    payload: Dict[str, Any] = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ],
        "inferenceConfig": {
            "maxTokens": 800,
            "temperature": 0.6,
        },
    }
    if system_prompt:
        payload["system"] = [{"text": system_prompt}]
        
    return json.dumps(payload).encode("utf-8")

# ─── Response Parser ─────────────────────────────────────────────────────────
def _parse_nova_response(response_body: Dict[str, Any]) -> str:
    """Parse text from Amazon Nova response."""
    try:
        return str(response_body["output"]["message"]["content"][0]["text"])
    except (KeyError, IndexError, TypeError):
        if "generation" in response_body:
            return str(response_body["generation"])
        return ""

# ─── Cache ───────────────────────────────────────────────────────────────────
_cache: Dict[str, str] = {}

# ─── Core Function ──────────────────────────────────────────────────────────
def invoke_model(prompt: str, system_prompt: Optional[str] = None) -> str:
    """Call Bedrock with caching and failover."""
    if len(_cache) > 200:
        _cache.clear()

    cache_key = f"{system_prompt or ''}:{prompt}"
    if cache_key in _cache:
        logger.info("[Cache] Hit!")
        return _cache[cache_key]

    try:
        client = get_bedrock_client()
    except Exception:
        return "AWS connection failed. Check credentials."
    
    models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]
    last_error = "All models failed"
    
    for model_id in models_to_try:
        if not model_id: continue
        
        try:
            logger.info(f"[Bedrock] Invoking {model_id}...")
            start_time = time.time()
            
            raw = client.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=_nova_body(prompt, system_prompt),
            )
            
            elapsed = time.time() - start_time
            body_content = raw["body"].read().decode("utf-8")
            response_body = json.loads(body_content)
            text = _parse_nova_response(response_body)

            if text.strip():
                logger.info(f"[Bedrock] Success | {model_id} | Time: {elapsed:.2f}s")
                _cache[cache_key] = text
                return text

        except Exception as e:
            last_error = str(e)
            # Fix for Pyre2 slice issue: enumerate+join instead of [:n]
            error_preview_chars: List[str] = [c for i, c in enumerate(last_error) if i < 200]
            error_preview: str = "".join(error_preview_chars)
            logger.error(f"[Bedrock] {model_id} failed: {error_preview}")
            
            # If hit account limit, don't keep trying other models
            if "ThrottlingException" in last_error or "Too many tokens" in last_error:
                return "AWS Bedrock Limit Reached: Too many tokens per day. Please wait before trying again."
            continue

    return "AI service temporarily unavailable."
