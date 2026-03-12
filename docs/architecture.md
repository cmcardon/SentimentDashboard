# Architecture

## Overview

The monorepo separates operational concerns into four layers:

- `jobs/*`: source ingestion and reproducible score computation
- `packages/*`: database, provider abstractions, schemas, and scoring logic
- `apps/api`: FastAPI read API for the dashboard
- `apps/web`: Next.js frontend with graceful fallback behavior when data is incomplete

## Data flow

1. Host definitions are loaded from `config/hosts.yaml`
2. Ingestion jobs call provider adapters and persist:
   - normalized daily fact tables
   - confidence-bearing mention matches
   - raw provider payloads in `raw_source_events`
3. Scoring jobs compute subscores and composite popularity scores into `host_scores_daily`
4. API routes read the latest normalized facts and expose dashboard-friendly payloads
5. The web app renders leaderboard, host detail, and compare views

## Production notes

- Providers stay behind interfaces so live vendors can be swapped without touching jobs or API consumers
- The UI is resilient to provider outages because every data source is optional at render time
- Cache entries are persisted to Postgres so quotas can be respected across job runs
- X and news providers are intentionally stubbed behind the same interface for later rollout

