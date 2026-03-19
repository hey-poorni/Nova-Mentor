import os
from dotenv import load_dotenv
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# --- Path Resolution ---
# Correctly find the project root (.env location)
# This finds the directory containing 'backend' or the current working directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env_path = BASE_DIR / ".env"

if env_path.exists():
    logger.info(f"Loading environment from {env_path}")
    load_dotenv(dotenv_path=env_path, override=True)
else:
    logger.warning(f".env file not found at {env_path}. Falling back to system environment variables.")
    load_dotenv(override=True)

# --- AWS Configuration ---
AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID", "").strip()
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "").strip()
AWS_DEFAULT_REGION    = os.getenv("AWS_DEFAULT_REGION", "us-east-1").strip()

# --- Model Configuration ---
# Allow overriding model IDs via env for flexibility
PRIMARY_MODEL         = os.getenv("MODEL_ID", "amazon.nova-micro-v1:0")
FALLBACK_MODEL        = os.getenv("FALLBACK_MODEL_ID", "amazon.nova-lite-v1:0")

# --- Validation ---
REQUIRED_VARS = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
missing = [var for var in REQUIRED_VARS if not globals().get(var)]

if missing:
    error_msg = f"CRITICAL: Missing required environment variables: {', '.join(missing)}"
    logger.error(error_msg)
    # Note: In production we might raise RuntimeError(error_msg) here

