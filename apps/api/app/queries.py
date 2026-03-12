from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from packages.db.models import (
    GoogleTrendsDaily,
    Host,
    HostScoreDaily,
    PodcastMentionsDaily,
    SentimentDocument,
    SerpRankDaily,
    YouTubeChannelDaily,
)


def get_latest_score_day(session: Session) -> Optional[date]:
    return session.scalar(select(func.max(HostScoreDaily.day)))


def fetch_leaderboard(session: Session, day: Optional[date] = None):
    score_day = day or get_latest_score_day(session)
    if score_day is None:
        return []

    youtube_subquery = (
        select(YouTubeChannelDaily.host_id, YouTubeChannelDaily.views)
        .where(YouTubeChannelDaily.day == score_day)
        .subquery()
    )
    trends_subquery = (
        select(GoogleTrendsDaily.host_id, GoogleTrendsDaily.interest_score)
        .where(GoogleTrendsDaily.day == score_day)
        .subquery()
    )
    serp_subquery = (
        select(SerpRankDaily.host_id, func.avg(SerpRankDaily.average_rank).label("avg_rank"))
        .where(SerpRankDaily.day == score_day)
        .group_by(SerpRankDaily.host_id)
        .subquery()
    )
    podcasts_subquery = (
        select(PodcastMentionsDaily.host_id, func.sum(PodcastMentionsDaily.mention_count).label("mentions"))
        .where(PodcastMentionsDaily.day == score_day)
        .group_by(PodcastMentionsDaily.host_id)
        .subquery()
    )

    query = (
        select(
            Host.slug,
            Host.name,
            HostScoreDaily.day,
            HostScoreDaily.popularity_score,
            HostScoreDaily.attention,
            HostScoreDaily.discoverability,
            HostScoreDaily.engagement,
            HostScoreDaily.sentiment,
            HostScoreDaily.crossover,
            HostScoreDaily.momentum_7d,
            HostScoreDaily.momentum_30d,
            youtube_subquery.c.views,
            trends_subquery.c.interest_score,
            serp_subquery.c.avg_rank,
            podcasts_subquery.c.mentions,
        )
        .join(Host, Host.id == HostScoreDaily.host_id)
        .outerjoin(youtube_subquery, youtube_subquery.c.host_id == Host.id)
        .outerjoin(trends_subquery, trends_subquery.c.host_id == Host.id)
        .outerjoin(serp_subquery, serp_subquery.c.host_id == Host.id)
        .outerjoin(podcasts_subquery, podcasts_subquery.c.host_id == Host.id)
        .where(HostScoreDaily.day == score_day)
        .order_by(HostScoreDaily.popularity_score.desc(), Host.name.asc())
    )
    return session.execute(query).all()


def fetch_host_detail(session: Session, slug: str):
    host = session.scalar(select(Host).where(Host.slug == slug))
    if host is None:
        return None
    score_day = get_latest_score_day(session)
    if score_day is None:
        return {"host": host, "leaderboard_row": None, "score_series": [], "trends_series": [], "youtube_series": [], "sentiment_series": [], "appearances": []}

    leaderboard_rows = fetch_leaderboard(session, score_day)
    leaderboard_row = next((row for row in leaderboard_rows if row.slug == slug), None)
    start_day = score_day - timedelta(days=29)

    score_series = session.execute(
        select(HostScoreDaily.day, HostScoreDaily.popularity_score)
        .where(HostScoreDaily.host_id == host.id, HostScoreDaily.day >= start_day)
        .order_by(HostScoreDaily.day.asc())
    ).all()
    trends_series = session.execute(
        select(GoogleTrendsDaily.day, GoogleTrendsDaily.interest_score)
        .where(GoogleTrendsDaily.host_id == host.id, GoogleTrendsDaily.day >= start_day)
        .order_by(GoogleTrendsDaily.day.asc())
    ).all()
    youtube_series = session.execute(
        select(YouTubeChannelDaily.day, YouTubeChannelDaily.views)
        .where(YouTubeChannelDaily.host_id == host.id, YouTubeChannelDaily.day >= start_day)
        .order_by(YouTubeChannelDaily.day.asc())
    ).all()
    sentiment_series = session.execute(
        select(SentimentDocument.day, func.avg(SentimentDocument.sentiment_score))
        .where(SentimentDocument.host_id == host.id, SentimentDocument.day >= start_day)
        .group_by(SentimentDocument.day)
        .order_by(SentimentDocument.day.asc())
    ).all()
    appearances = session.execute(
        select(
            PodcastMentionsDaily.day,
            PodcastMentionsDaily.podcast_name,
            PodcastMentionsDaily.episode_title,
            PodcastMentionsDaily.confidence,
        )
        .where(PodcastMentionsDaily.host_id == host.id, PodcastMentionsDaily.day >= start_day)
        .order_by(PodcastMentionsDaily.day.desc())
        .limit(25)
    ).all()
    return {
        "host": host,
        "leaderboard_row": leaderboard_row,
        "score_series": score_series,
        "trends_series": trends_series,
        "youtube_series": youtube_series,
        "sentiment_series": sentiment_series,
        "appearances": appearances,
    }
