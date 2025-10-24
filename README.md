# Sharkflow MVP — Data → AI → SQL Workflow

This is a **zero-dependency** (well, just Python deps) starter you can run locally to test your workflow end-to-end:

- Upload or import your **CSV** data
- Run an **AI processing step** (currently a safe stub; hook in OpenAI if you want)
- Store normalized records in **SQLite**
- Use a simple **web form** and **REST API** to trigger processing
- Ready to later swap SQLite → Postgres / Supabase, add auth, and Stripe for SaaS

---

## Quick Start

### 1) Create a virtual env & install deps
```bash
cd sharkflow-mvp
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Initialize the database
```bash
python scripts/init_db.py
```

### 3) (Optional) Import your CSV
Put CSVs into `./data/`. Then run:
```bash
python scripts/import_csv.py --file data/sample.csv --mapping config/field_mapping.json
```

### 4) Run the app
```bash
uvicorn app:app --reload
```
Open http://127.0.0.1:8000 in your browser.

---

## Project Structure

```
sharkflow-mvp/
├─ app.py                  # FastAPI app (UI + API)
├─ ai.py                   # AI processing (stub + OpenAI hook)
├─ db.py                   # DB helpers (SQLite now)
├─ models.py               # Pydantic models
├─ requirements.txt
├─ templates/
│  └─ index.html           # Simple UI
├─ static/
│  └─ styles.css
├─ scripts/
│  ├─ init_db.py           # Create tables
│  └─ import_csv.py        # CSV → SQLite with mapping
├─ config/
│  └─ field_mapping.json   # Map your CSV → canonical schema
├─ data/
│  └─ sample.csv           # Example data
└─ .env.example            # Where to put OPENAI_API_KEY if you enable real AI
```

---

## Enabling Real AI (OpenAI)

1) Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
2) In `ai.py`, set `USE_OPENAI = True` and customize the prompt in `run_ai_enrichment`.

> The code uses the official `openai` Python SDK. You can also swap in any LLM provider.

---

## Switching to Postgres / Supabase

- Replace `sqlite:///sharkflow.db` DSN in `db.py` with a Postgres DSN, e.g. `postgresql+psycopg://user:pass@host:5432/db`.
- Install `psycopg[binary]` and update `requirements.txt`.
- Run the same `scripts/init_db.py` against your Postgres DB.

---

## Next Steps for SaaS

- Add user auth (e.g., Supabase Auth) and per-tenant scoping
- Stripe subscriptions + metered billing
- Background workers (RQ/Celery) for large imports
- Admin dashboard for workflow runs & errors
- Export results to email, Webhook, or PDF

---

*Generated on 2025-10-23*
