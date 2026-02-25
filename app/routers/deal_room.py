from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from app.db import get_session
from app.models import Deal
from app.services.token import read_token

router = APIRouter()

env = Environment(loader=FileSystemLoader("app/templates"))

@router.get("/deal-room/{token}", response_class=HTMLResponse)
async def deal_room(token: str, session: AsyncSession = Depends(get_session)):
    try:
        data = read_token(token)
        deal_id = data.get("deal_id")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")

    deal = (await session.execute(select(Deal).where(Deal.id == deal_id))).scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    tmpl = env.get_template("deal_room.html")
    html = tmpl.render(
        address=deal.address,
        city=deal.city,
        state=deal.state,
        list_price=deal.list_price or "N/A",
        arv=deal.arv or "N/A",
        repairs=deal.repairs or "N/A",
        mao=deal.mao or "N/A",
        score=deal.score,
        status=deal.status,
    )
    return HTMLResponse(html)
