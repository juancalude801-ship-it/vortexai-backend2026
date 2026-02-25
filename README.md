# VortexAI Lite (Dallas-only) — FastAPI + Supabase + Railway

This is a clean, minimal backend you can deploy to Railway and connect to Supabase.

You described:
- Press a button → pull leads → show GREEN/ORANGE/RED
- You call/email sellers yourself
- When you have a deal, you pull your buyers list

This repo gives you that *core* workflow.

## 1) Create Supabase tables
Open Supabase → SQL Editor → run:

- `supabase/schema.sql`

## 2) Set Railway Variables (or local .env)
- `SUPABASE_URL`
- `SUPABASE_KEY`  (recommended: **Service Role key** on Railway)
- `USE_SAMPLE_DATA=true`
- `DEFAULT_CITY=Dallas`

## 3) Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

## 4) Deploy to Railway
- Push to GitHub
- Railway → New Project → Deploy from GitHub
- Add Variables above
- It will run on port 8080

## Endpoints
- `GET /health`
- `POST /pull-deals`  (inserts sample leads into Supabase with scoring)
- `GET /leads?limit=200&status=new`
- `POST /leads/{lead_id}/status` body: `{"status":"contacted","notes":"called"}`
- `POST /buyers` body: `{"name":"Buyer A","phone":"+1...","city":"Dallas","zip_codes":"75201,75202","max_price":350000}`
- `GET /buyers?city=Dallas`
- `POST /deals/{lead_id}/blast-buyers` body: `{"message":"Deal summary here"}`

## Next step (after this runs)
Replace the sample data generator in `app/sources.py` with your RentCast pull + filters.
