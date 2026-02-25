import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.db import SessionLocal
from app.models import Deal
from app.services.scoring import score_to_bucket
from app.services.brevo_email import send_email

async def run_cycle():
    # This cycle just emails a "daily report" of green deals to REPORT_EMAIL
    # Ingest is triggered via /deals/ingest or you can add ingest here later.

    if not settings.REPORT_EMAIL:
        return {"skipped": True, "reason": "REPORT_EMAIL not set"}

    async with SessionLocal() as session:  # type: AsyncSession
        res = await session.execute(select(Deal).order_by(Deal.created_at.desc()).limit(50))
        deals = list(res.scalars().all())

        greens = [d for d in deals if score_to_bucket(d.score) == "green"]
        if not greens:
            return {"green_count": 0, "email_sent": False}

        html = "<h2>Green Deals Report</h2><ul>"
        for d in greens[:25]:
            html += f"<li>{d.address}, {d.city} {d.state} — Score {d.score} — Price {d.list_price or 'N/A'}</li>"
        html += "</ul>"

        await send_email(settings.REPORT_EMAIL, "✅ VortexAI Green Deals Report", html)
        return {"green_count": len(greens), "email_sent": True}

async def start_worker():
    if not settings.AUTORUN_ENABLED:
        return

    while True:
        try:
            await run_cycle()
        except Exception as e:
            print("[Worker] Error:", e)
        await asyncio.sleep(settings.AUTORUN_INTERVAL_SECONDS)
