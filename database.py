from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY

def get_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in environment variables.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)
