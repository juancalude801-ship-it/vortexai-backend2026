import asyncio
from fastapi import FastAPI
from app.db import init_db
from app.routers.health import router as health_router
from app.routers.buyers import router as buyers_router
from app.routers.sellers import router as sellers_router
from app.routers.deals import router as deals_router
from app.jobs.worker import start_worker

app = FastAPI(title="VortexAI Wholesale Engine")

app.include_router(health_router)
app.include_router(buyers_router, prefix="/buyers", tags=["buyers"])
app.include_router(sellers_router, prefix="/sellers", tags=["sellers"])
app.include_router(deals_router, prefix="/deals", tags=["deals"])

@app.on_event("startup")
async def startup():
    await init_db()
    # Start background worker loop
    asyncio.create_task(start_worker())
