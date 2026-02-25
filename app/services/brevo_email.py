import httpx
from app.config import settings

BREVO_URL = "https://api.brevo.com/v3/smtp/email"

async def send_email(to_email: str, subject: str, html: str):
    if not settings.BREVO_API_KEY:
        return {"skipped": True, "reason": "BREVO_API_KEY not set"}

    payload = {
        "sender": {"name": settings.BREVO_SENDER_NAME, "email": settings.BREVO_SENDER_EMAIL},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html,
    }
    headers = {"api-key": settings.BREVO_API_KEY, "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(BREVO_URL, headers=headers, json=payload)
        r.raise_for_status()
        return r.json()
