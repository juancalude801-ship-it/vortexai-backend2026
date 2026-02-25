import csv
import io
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_session
from app.models import Buyer
from app.schemas import BuyerCreate, BuyerOut

router = APIRouter()

@router.post("", response_model=BuyerOut)
async def create_buyer(payload: BuyerCreate, session: AsyncSession = Depends(get_session)):
    buyer = Buyer(**payload.model_dump())
    session.add(buyer)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        # If duplicate constraint triggered, return existing
        q = select(Buyer).where(Buyer.email == payload.email, Buyer.city == payload.city, Buyer.state == payload.state)
        res = await session.execute(q)
        existing = res.scalar_one_or_none()
        if existing:
            return existing
        raise
    await session.refresh(buyer)
    return buyer

@router.get("", response_model=list[BuyerOut])
async def list_buyers(
    city: str | None = Query(default=None),
    state: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    q = select(Buyer)
    if city:
        q = q.where(Buyer.city.ilike(city))
    if state:
        q = q.where(Buyer.state.ilike(state))
    res = await session.execute(q)
    return list(res.scalars().all())

@router.post("/import-csv")
async def import_buyers_csv(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))

    inserted = 0
    skipped = 0
    for row in reader:
        email = (row.get("email") or "").strip()
        if not email:
            skipped += 1
            continue

        buyer = Buyer(
            full_name=(row.get("full_name") or row.get("name") or "").strip() or "Buyer",
            email=email,
            phone=(row.get("phone") or "").strip() or None,
            city=(row.get("city") or "").strip(),
            state=(row.get("state") or "").strip(),
            min_price=int(row["min_price"]) if row.get("min_price") else None,
            max_price=int(row["max_price"]) if row.get("max_price") else None,
            strategy=(row.get("strategy") or "").strip() or None
        )
        session.add(buyer)
        try:
            await session.commit()
            inserted += 1
        except Exception:
            await session.rollback()
            skipped += 1

    return {"inserted": inserted, "skipped": skipped}
