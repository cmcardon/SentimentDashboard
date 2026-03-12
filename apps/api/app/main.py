from __future__ import annotations

from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from apps.api.app.queries import fetch_host_detail, fetch_leaderboard
from packages.db.session import get_db
from packages.schemas.api import AppearancePoint, HealthResponse, HostDetailResponse, LeaderboardRow, TimeSeriesPoint


app = FastAPI(title="Sentiment Dashboard API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(timestamp=datetime.now(timezone.utc))


@app.get("/api/leaderboard", response_model=list[LeaderboardRow])
def leaderboard(db: Session = Depends(get_db)):
    rows = fetch_leaderboard(db)
    return [
        LeaderboardRow(
            host_slug=row.slug,
            host_name=row.name,
            score_date=row.day,
            popularity_score=row.popularity_score,
            attention=row.attention,
            discoverability=row.discoverability,
            engagement=row.engagement,
            sentiment=row.sentiment,
            crossover=row.crossover,
            momentum_7d=row.momentum_7d,
            momentum_30d=row.momentum_30d,
            youtube_views=row.views,
            google_trends_interest=row.interest_score,
            serp_avg_rank=row.avg_rank,
            podcast_mentions=row.mentions,
        )
        for row in rows
    ]


@app.get("/api/hosts/{slug}", response_model=HostDetailResponse)
def host_detail(slug: str, db: Session = Depends(get_db)):
    data = fetch_host_detail(db, slug)
    if data is None or data["leaderboard_row"] is None:
        raise HTTPException(status_code=404, detail="Host not found")
    row = data["leaderboard_row"]
    return HostDetailResponse(
        host_slug=data["host"].slug,
        host_name=data["host"].name,
        leaderboard=LeaderboardRow(
            host_slug=row.slug,
            host_name=row.name,
            score_date=row.day,
            popularity_score=row.popularity_score,
            attention=row.attention,
            discoverability=row.discoverability,
            engagement=row.engagement,
            sentiment=row.sentiment,
            crossover=row.crossover,
            momentum_7d=row.momentum_7d,
            momentum_30d=row.momentum_30d,
            youtube_views=row.views,
            google_trends_interest=row.interest_score,
            serp_avg_rank=row.avg_rank,
            podcast_mentions=row.mentions,
        ),
        score_series=[TimeSeriesPoint(day=day, value=value) for day, value in data["score_series"]],
        trends_series=[TimeSeriesPoint(day=day, value=value) for day, value in data["trends_series"]],
        youtube_series=[TimeSeriesPoint(day=day, value=float(value)) for day, value in data["youtube_series"]],
        sentiment_series=[TimeSeriesPoint(day=day, value=float(value or 0)) for day, value in data["sentiment_series"]],
        appearances=[
            AppearancePoint(day=day, source=podcast_name, title=episode_title, confidence=confidence)
            for day, podcast_name, episode_title, confidence in data["appearances"]
        ],
    )

