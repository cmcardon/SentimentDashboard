from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import yaml
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from packages.db.models import (
    GoogleTrendsDaily,
    Host,
    HostAlias,
    HostScoreDaily,
    PlatformAccount,
    PodcastMentionsDaily,
    SentimentDocument,
    SerpRankDaily,
    YouTubeChannelDaily,
    YouTubeVideoDaily,
)
from packages.providers.matching import normalize_alias
from packages.scoring.core import compute_composite_score, compute_momentum


@dataclass
class HostConfig:
    slug: str
    name: str
    description: Optional[str]
    aliases: list[str]
    platforms: list[dict[str, Any]]
    metadata: dict[str, Any]


def load_host_configs(config_path: str | Path = "config/hosts.yaml") -> list[HostConfig]:
    with open(config_path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    hosts = []
    for item in data.get("hosts", []):
        hosts.append(
            HostConfig(
                slug=item["slug"],
                name=item["name"],
                description=item.get("description"),
                aliases=item.get("aliases", []),
                platforms=item.get("platform_accounts", []),
                metadata=item.get("metadata", {}),
            )
        )
    return hosts


def seed_hosts(session: Session, config_path: str | Path = "config/hosts.yaml") -> None:
    for host_cfg in load_host_configs(config_path):
        host = session.scalar(select(Host).where(Host.slug == host_cfg.slug))
        if host is None:
            host = Host(slug=host_cfg.slug, name=host_cfg.name, description=host_cfg.description, config_metadata=host_cfg.metadata)
            session.add(host)
            session.flush()
        else:
            host.name = host_cfg.name
            host.description = host_cfg.description
            host.config_metadata = host_cfg.metadata

        existing_aliases = {alias.alias for alias in host.aliases}
        desired_aliases = {normalize_alias(host_cfg.name), *(normalize_alias(alias) for alias in host_cfg.aliases)}
        for alias in desired_aliases - existing_aliases:
            session.add(HostAlias(host_id=host.id, alias=alias, alias_type="config"))

        existing_accounts = {(account.platform, account.account_id) for account in host.accounts}
        for account in host_cfg.platforms:
            key = (account["platform"], account["account_id"])
            if key in existing_accounts:
                continue
            session.add(
                PlatformAccount(
                    host_id=host.id,
                    platform=account["platform"],
                    account_id=account["account_id"],
                    username=account.get("username"),
                    url=account.get("url"),
                    account_metadata=account.get("metadata", {}),
                )
            )
    session.commit()


def seed_mock_metrics(session: Session, lookback_days: int = 45) -> None:
    hosts = session.scalars(select(Host).order_by(Host.id)).all()
    if not hosts:
        return

    for model in (
        YouTubeVideoDaily,
        YouTubeChannelDaily,
        GoogleTrendsDaily,
        SerpRankDaily,
        PodcastMentionsDaily,
        SentimentDocument,
        HostScoreDaily,
    ):
        session.execute(delete(model))
    session.commit()

    today = date.today()
    for idx, host in enumerate(hosts, start=1):
        popularity_series: list[float] = []
        for offset in range(lookback_days):
            day = today - timedelta(days=(lookback_days - 1 - offset))
            trend_boost = idx * 2 + offset * 0.4
            views = int(15000 + idx * 2500 + offset * 350)
            subscribers = int(200000 + idx * 15000 + offset * 125)
            videos_published = 1 if offset % 6 == 0 else 0
            interest = min(100.0, 35 + trend_boost)
            avg_rank = max(1.0, 15 - idx - offset * 0.08)
            mention_count = 1 + ((offset + idx) % 4)
            sentiment_score = max(-1.0, min(1.0, -0.1 + idx * 0.18 + offset * 0.006))

            session.add(
                YouTubeChannelDaily(
                    host_id=host.id,
                    day=day,
                    views=views,
                    subscribers=subscribers,
                    videos_published=videos_published,
                    source_metadata={"provider": "mock_youtube"},
                    raw_payload={"views": views, "subscribers": subscribers},
                )
            )
            session.add(
                YouTubeVideoDaily(
                    host_id=host.id,
                    video_id=f"{host.slug}-{day.isoformat()}",
                    day=day,
                    title=f"{host.name} segment for {day.isoformat()}",
                    views=views // 4,
                    likes=views // 80,
                    comments=views // 250,
                    engagement_rate=4.8 + idx * 0.35,
                    source_metadata={"provider": "mock_youtube"},
                    raw_payload={"video_id": f"{host.slug}-{day.isoformat()}"},
                )
            )
            session.add(
                GoogleTrendsDaily(
                    host_id=host.id,
                    day=day,
                    interest_score=interest,
                    source_metadata={"provider": "mock_google_trends"},
                    raw_payload={"interest": interest},
                )
            )
            session.add(
                SerpRankDaily(
                    host_id=host.id,
                    keyword=host.name,
                    day=day,
                    average_rank=avg_rank,
                    best_rank=int(avg_rank),
                    confidence=0.92,
                    source_metadata={"provider": "mock_serp"},
                    raw_payload={"average_rank": avg_rank},
                )
            )
            session.add(
                PodcastMentionsDaily(
                    host_id=host.id,
                    episode_id=f"{host.slug}-pod-{day.isoformat()}",
                    day=day,
                    podcast_name="BlazeTV Daily Roundup",
                    episode_title=f"{host.name} mention on {day.isoformat()}",
                    mention_count=mention_count,
                    confidence=0.88,
                    source_metadata={"provider": "mock_listen_notes"},
                    raw_payload={"mentions": mention_count},
                )
            )
            session.add(
                SentimentDocument(
                    host_id=host.id,
                    source="podcasts",
                    source_document_id=f"{host.slug}-sent-{day.isoformat()}",
                    published_at=datetime.combine(day, datetime.min.time(), tzinfo=timezone.utc),
                    day=day,
                    title=f"{host.name} audience reaction",
                    excerpt="Mock sentiment sample for local development",
                    sentiment_label="positive" if sentiment_score >= 0 else "negative",
                    sentiment_score=sentiment_score,
                    confidence=0.84,
                    source_metadata={"provider": "mock_sentiment"},
                    raw_payload={"sentiment_score": sentiment_score},
                )
            )

            attention = min(100.0, views / 300.0)
            discoverability = max(0.0, min(100.0, (110 - (avg_rank * 6)) * 0.9 + interest * 0.25))
            engagement = min(100.0, 35 + (views / 2000.0) + (mention_count * 4))
            sentiment = max(0.0, min(100.0, (sentiment_score + 1) * 50))
            crossover = min(100.0, 20 + mention_count * 10 + interest * 0.3)
            popularity = compute_composite_score(attention, discoverability, engagement, sentiment, crossover)
            popularity_series.append(popularity)
            momentum_7d = compute_momentum(popularity_series, 7)
            momentum_30d = compute_momentum(popularity_series, 30)

            session.add(
                HostScoreDaily(
                    host_id=host.id,
                    day=day,
                    attention=attention,
                    discoverability=discoverability,
                    engagement=engagement,
                    sentiment=sentiment,
                    crossover=crossover,
                    popularity_score=popularity,
                    momentum_7d=momentum_7d,
                    momentum_30d=momentum_30d,
                    source_metadata={"method": "mock_seed_v1"},
                )
            )
    session.commit()
