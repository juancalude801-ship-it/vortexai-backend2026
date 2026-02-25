from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_session
from app.models import Deal, Buyer, ContractFile
from app.schemas import DealOut, UnderwriteRequest
from app.services.rentcast import fetch_listings
from app.services.scoring import score_deal, score_to_bucket
from app.services.matching import buyer_matches_deal
from app.services.brevo_email import send_email
from app.services.token import make_token, read_token
from app.services.contract_pdf import build_contract_pdf
from app.config import settings

router = APIRouter()

def parse_markets():
    markets = []
    for part in settings.MARKETS.split("|"):
        part = part.strip()
        if not part:
            continue
        city_state = part.split(",")
        if len(city_state) != 2:
            continue
        markets.append((city_state[0].strip(), city_state[1].strip()))
    return markets

@router.post("/ingest")
async def ingest(session: AsyncSession = Depends(get_session)):
    markets = parse_markets()
    created = 0

    for (city, state) in markets:
        data = await fetch_listings(city, state, limit=25)

        # Expecting data list shape; adapt if RentCast returns dict
        items = data if isinstance(data, list) else data.get("listings") or data.get("data") or []

        for item in items:
            address = item.get("formattedAddress") or item.get("address") or "Unknown Address"
            zipcode = item.get("zipCode") or item.get("zipcode")
            list_price = item.get("price") or item.get("listPrice")
            beds = item.get("bedrooms")
            baths = item.get("bathrooms")
            sqft = item.get("squareFootage") or item.get("sqft")
            year_built = item.get("yearBuilt")
            ptype = item.get("propertyType")

            # prevent duplicates by address+city+state
            q = select(Deal).where(Deal.address == address, Deal.city == city, Deal.state == state)
            res = await session.execute(q)
            existing = res.scalar_one_or_none()
            if existing:
                continue

            deal = Deal(
                address=address,
                city=city,
                state=state,
                zipcode=str(zipcode) if zipcode else None,
                list_price=int(list_price) if list_price else None,
                beds=int(beds) if beds else None,
                baths=float(baths) if baths else None,
                sqft=int(sqft) if sqft else None,
                year_built=int(year_built) if year_built else None,
                property_type=str(ptype) if ptype else None,
            )

            # MVP scoring (needs ARV to score well; we can later enrich comps)
            deal.score = score_deal(deal.list_price, deal.arv, deal.repairs)
            deal.status = score_to_bucket(deal.score)

            session.add(deal)
            await session.commit()
            created += 1

    return {"created": created, "markets": len(markets)}

@router.get("", response_model=list[DealOut])
async def list_deals(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Deal).order_by(Deal.created_at.desc()))
    return list(res.scalars().all())

@router.post("/{deal_id}/underwrite")
async def underwrite(deal_id: int, payload: UnderwriteRequest, session: AsyncSession = Depends(get_session)):
    deal = (await session.execute(select(Deal).where(Deal.id == deal_id))).scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    # Apply ARV/repairs inputs
    if payload.arv is not None:
        deal.arv = payload.arv
    if payload.repairs is not None:
        deal.repairs = payload.repairs

    # MAO = (ARV * rule) - repairs - assignment_fee
    if deal.arv:
        rule = payload.investor_rule or 0.70
        fee = payload.assignment_fee or 10000
        repairs = deal.repairs or 0
        deal.mao = int((deal.arv * rule) - repairs - fee)

    deal.score = score_deal(deal.list_price, deal.arv, deal.repairs)
    deal.status = score_to_bucket(deal.score)

    await session.commit()
    return {"ok": True, "deal_id": deal.id, "score": deal.score, "status": deal.status, "mao": deal.mao}

@router.post("/{deal_id}/blast")
async def blast_buyers(deal_id: int, session: AsyncSession = Depends(get_session)):
    deal = (await session.execute(select(Deal).where(Deal.id == deal_id))).scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    buyers = (await session.execute(select(Buyer))).scalars().all()
    matched = [b for b in buyers if buyer_matches_deal(b, deal)]

    token = make_token({"deal_id": deal.id})
    deal_room_url = f"{settings.BASE_URL}/deal-room/{token}"

    subject = f"🔥 Off-Market Style Deal in {deal.city}, {deal.state} (Score {deal.score})"
    html = f"""
    <h2>New Deal Opportunity</h2>
    <p><b>Address:</b> {deal.address}, {deal.city}, {deal.state} {deal.zipcode or ""}</p>
    <p><b>List Price:</b> {deal.list_price or "N/A"}</p>
    <p><b>ARV:</b> {deal.arv or "N/A"} | <b>Repairs:</b> {deal.repairs or "N/A"} | <b>MAO:</b> {deal.mao or "N/A"}</p>
    <p><b>Score:</b> {deal.score} ({deal.status})</p>
    <p><a href="{deal_room_url}">View Deal Room</a></p>
    <hr/>
    <p>Reply to this email to claim the deal.</p>
    """

    sent = 0
    for b in matched:
        await send_email(b.email, subject, html)
        sent += 1

    deal.last_blasted_at = datetime.utcnow()
    deal.status = "blasted"
    await session.commit()

    return {"ok": True, "matched": len(matched), "emails_sent": sent, "deal_room": deal_room_url}

@router.post("/{deal_id}/contract")
async def contract(deal_id: int, session: AsyncSession = Depends(get_session)):
    deal = (await session.execute(select(Deal).where(Deal.id == deal_id))).scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    pdf_bytes = build_contract_pdf({
        "Deal ID": deal.id,
        "Address": f"{deal.address}, {deal.city}, {deal.state}",
        "List Price": deal.list_price,
        "ARV": deal.arv,
        "Repairs": deal.repairs,
        "MAO": deal.mao,
        "Score": deal.score,
        "Status": deal.status,
    })

    filename = f"contract_deal_{deal.id}.pdf"
    cf = ContractFile(deal_id=deal.id, filename=filename)
    session.add(cf)
    await session.commit()

    return Response(content=pdf_bytes, media_type="application/pdf")
