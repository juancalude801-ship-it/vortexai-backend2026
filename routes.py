from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.config import DEFAULT_CITY, USE_SAMPLE_DATA
from app.database import get_supabase
from app.sources import get_sample_deals
from app.scoring import calculate_mao, calculate_spread, score_deal

router = APIRouter()

class StatusUpdate(BaseModel):
    status: str = Field(..., description="new/contacted/offer_sent/contract_signed/dead")
    notes: Optional[str] = None

class BuyerCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    city: str = DEFAULT_CITY
    zip_codes: Optional[str] = ""
    max_price: Optional[float] = None
    notes: Optional[str] = None

class BlastRequest(BaseModel):
    message: str

@router.post("/pull-deals")
def pull_deals(limit: int = 20, city: str = DEFAULT_CITY):
    sb = get_supabase()

    if not USE_SAMPLE_DATA:
        raise HTTPException(status_code=400, detail="USE_SAMPLE_DATA is false, but RentCast pull is not implemented yet.")

    raw = get_sample_deals(city=city)[:limit]
    inserted = 0
    leads_out = []

    for p in raw:
        arv = float(p.get("arv") or 0)
        repairs = float(p.get("estimated_repairs") or 0)
        asking = float(p.get("asking_price") or 0)
        equity = float(p.get("equity_percent") or 0)

        mao = calculate_mao(arv, repairs)
        spread = calculate_spread(mao, asking)
        scored = score_deal(
            mao=mao,
            spread=spread,
            equity_percent=equity,
            dom_90_plus=bool(p.get("dom_90_plus")),
            price_drop=bool(p.get("price_drop")),
        )

        row = {
            "address": p.get("address"),
            "city": p.get("city", city),
            "zip": p.get("zip", ""),
            "owner_name": p.get("owner_name", ""),
            "phone": p.get("phone", ""),
            "asking_price": asking,
            "arv": arv,
            "estimated_repairs": repairs,
            "offer_price": scored.mao,
            "potential_spread": scored.spread,
            "equity_percent": equity,
            "score": scored.score,
            "color": scored.color,
            "status": "new",
        }

        sb.table("sellers").insert(row).execute()
        inserted += 1
        leads_out.append(row)

    return {"city": city, "inserted": inserted, "leads": leads_out}

@router.get("/leads")
def list_leads(limit: int = 200, city: Optional[str] = DEFAULT_CITY, status: Optional[str] = None):
    sb = get_supabase()
    q = sb.table("sellers").select("*").order("created_at", desc=True).limit(limit)
    if city:
        q = q.eq("city", city)
    if status:
        q = q.eq("status", status)
    res = q.execute()
    return {"count": len(res.data or []), "leads": res.data or []}

@router.post("/leads/{lead_id}/status")
def update_lead_status(lead_id: str, body: StatusUpdate):
    sb = get_supabase()
    update = {"status": body.status}
    if body.notes is not None:
        update["notes"] = body.notes
    res = sb.table("sellers").update(update).eq("id", lead_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"updated": res.data[0]}

@router.post("/buyers")
def create_buyer(body: BuyerCreate):
    sb = get_supabase()
    res = sb.table("buyers").insert(body.model_dump()).execute()
    return {"buyer": (res.data[0] if res.data else None)}

@router.get("/buyers")
def list_buyers(limit: int = 500, city: Optional[str] = DEFAULT_CITY):
    sb = get_supabase()
    q = sb.table("buyers").select("*").order("created_at", desc=True).limit(limit)
    if city:
        q = q.eq("city", city)
    res = q.execute()
    return {"count": len(res.data or []), "buyers": res.data or []}

@router.post("/deals/{lead_id}/blast-buyers")
def blast_buyers(lead_id: str, body: BlastRequest, city: str = DEFAULT_CITY):
    """No email/SMS sending yet.
    This returns the lead + buyers list so you can copy/paste and send manually.
    """
    sb = get_supabase()

    lead_res = sb.table("sellers").select("*").eq("id", lead_id).limit(1).execute()
    if not lead_res.data:
        raise HTTPException(status_code=404, detail="Lead not found")

    buyers_res = sb.table("buyers").select("*").eq("city", city).limit(500).execute()

    return {
        "lead": lead_res.data[0],
        "buyers_count": len(buyers_res.data or []),
        "buyers": buyers_res.data or [],
        "message": body.message,
    }
