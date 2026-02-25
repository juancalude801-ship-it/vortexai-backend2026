import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

USE_SAMPLE_DATA = os.getenv("USE_SAMPLE_DATA", "true").lower() in ("1", "true", "yes", "y")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Dallas").strip()
