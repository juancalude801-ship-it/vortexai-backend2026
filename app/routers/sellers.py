from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models import SellerLead
from app.schemas import SellerIntake

router = APIRouter()

@router.post("/intake")
async def seller_intake(payload: SellerIntake, session: AsyncSession = Depends(get_session)):
    lead = SellerLead(**payload.model_dump())
    session.add(lead)
    await session.commit()
    return {"ok": True, "lead_id": lead.id}
