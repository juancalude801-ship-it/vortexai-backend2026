# VortexAI Wholesale Engine (FastAPI + Supabase + RentCast + Brevo)

## What this does
- Ingest listings from RentCast for configured markets
- Score deals 0-100
- Match deals to buyers by city/state + price range
- Blast "Green" deals to matched buyers via Brevo
- Deal room link with signed token
- Contract PDF generator
- Auto worker loop (runs every N seconds)

## Deploy (Railway)
1. Create Railway project
2. Add Postgres (or use Supabase)
3. Set environment variables in Railway:
   - DATABASE_URL
   - RENTCAST_API_KEY
   - BREVO_API_KEY
   - BREVO_SENDER_EMAIL
   - BREVO_SENDER_NAME
   - REPORT_EMAIL
   - MARKETS
   - AUTORUN_ENABLED
   - AUTORUN_INTERVAL_SECONDS
   - MIN_SCORE_TO_BLAST
   - DEAL_ROOM_SECRET
4. Deploy

## Endpoints
- GET /health
- POST /buyers
- GET /buyers
- POST /buyers/import-csv
- POST /sellers/intake
- POST /deals/ingest
- GET /deals
- POST /deals/{deal_id}/underwrite
- POST /deals/{deal_id}/blast
- GET /deal-room/{token}
- POST /deals/{deal_id}/contract

## Run locally
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
