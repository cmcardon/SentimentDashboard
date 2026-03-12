# Sentiment Dashboard

Internal BlazeTV host popularity dashboard built as a full-stack monorepo with Python jobs, FastAPI, Postgres, and Next.js.

## What is included in v0.1

- Config-driven host definitions from `config/hosts.yaml`
- Postgres schema and SQL migration
- Seed flow for hosts and mock daily metrics
- Provider interfaces for YouTube, Google Trends, SERP, podcasts, X, and news
- Quota-aware provider caching contract
- FastAPI leaderboard and host detail endpoints
- Next.js leaderboard, host detail, and compare pages
- Docker Compose for local Postgres, API, jobs, and web
- Tests for alias matching, score normalization, and API routes

## Monorepo layout

```text
apps/
  api/
  web/
jobs/
  ingest_youtube/
  ingest_google_trends/
  ingest_serp/
  ingest_podcasts/
  compute_sentiment/
  compute_scores/
packages/
  db/
  providers/
  scoring/
  schemas/
config/
docs/
migrations/
fixtures/
tests/
```

## Quick start

1. Copy `.env.example` to `.env`
2. Update API keys if available. The app can still run on mock providers without them.
3. Start the stack:

```bash
docker compose up --build
```

4. Apply migrations and seed data:

```bash
python3 scripts/run_migrations.py
python3 scripts/seed_all.py
```

5. Open the apps:

- API: `http://localhost:8000`
- Web: `http://localhost:3000`

## Local Python workflow without Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn apps.api.app.main:app --reload
```

## Notes

- Provider calls are always routed through interfaces in `packages/providers`
- Raw payloads are stored for auditability
- Google Search HTML is not scraped directly when a SERP provider is configured
- Scoring is deterministic and reproducible from normalized host-day facts

