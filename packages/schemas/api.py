from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    timestamp: datetime


class LeaderboardRow(BaseModel):
    host_slug: str
    host_name: str
    score_date: date
    popularity_score: float
    attention: float
    discoverability: float
    engagement: float
    sentiment: float
    crossover: float
    momentum_7d: Optional[float] = None
    momentum_30d: Optional[float] = None
    youtube_views: Optional[int] = None
    google_trends_interest: Optional[float] = None
    serp_avg_rank: Optional[float] = None
    podcast_mentions: Optional[int] = None


class TimeSeriesPoint(BaseModel):
    day: date
    value: float
    meta: dict[str, Any] = Field(default_factory=dict)


class AppearancePoint(BaseModel):
    day: date
    source: str
    title: str
    confidence: float


class HostDetailResponse(BaseModel):
    host_slug: str
    host_name: str
    leaderboard: LeaderboardRow
    score_series: list[TimeSeriesPoint]
    trends_series: list[TimeSeriesPoint]
    youtube_series: list[TimeSeriesPoint]
    sentiment_series: list[TimeSeriesPoint]
    appearances: list[AppearancePoint]
