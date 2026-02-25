from itsdangerous import URLSafeSerializer
from app.config import settings

def make_token(data: dict) -> str:
    s = URLSafeSerializer(settings.DEAL_ROOM_SECRET)
    return s.dumps(data)

def read_token(token: str) -> dict:
    s = URLSafeSerializer(settings.DEAL_ROOM_SECRET)
    return s.loads(token)
