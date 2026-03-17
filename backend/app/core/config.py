import os
from dotenv import load_dotenv

# Load .env with override so values are always fresh
load_dotenv(override=True)

AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID", "").strip()
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "").strip()
AWS_DEFAULT_REGION    = os.getenv("AWS_DEFAULT_REGION", "us-east-1").strip()
