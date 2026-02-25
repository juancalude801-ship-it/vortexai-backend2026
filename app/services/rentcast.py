import httpx
from app.config import settings

async def fetch_listings(city: str, state: str, limit: int = 25):
    # RentCast has multiple endpoints; this is a generic placeholder pull.
    # If your RentCast endpoint differs, change only this function.
    url = f"{settings.RENTCAST_BASE_URL}/listings/sale"
    headers = {"X-Api-Key": settings.RENTCAST_API_KEY}

    params = {"city": city, "state": state, "limit": limit}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, headers=headers, params=params)
        r.raise_for_status()
        return r.json()
