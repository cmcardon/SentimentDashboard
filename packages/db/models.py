from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from packages.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Host(TimestampMixin, Base):
    __tablename__ = "hosts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    config_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    aliases: Mapped[list["HostAlias"]] = relationship(back_populates="host", cascade="all, delete-orphan")
    accounts: Mapped[list["PlatformAccount"]] = relationship(back_populates="host", cascade="all, delete-orphan")


class HostAlias(TimestampMixin, Base):
    __tablename__ = "host_aliases"
    __table_args__ = (UniqueConstraint("host_id", "alias", name="uq_host_alias"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False, index=True)
    alias: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alias_type: Mapped[str] = mapped_column(String(50), default="name", nullable=False)

    host: Mapped[Host] = relationship(back_populates="aliases")


class PlatformAccount(TimestampMixin, Base):
    __tablename__ = "platform_accounts"
    __table_args__ = (UniqueConstraint("host_id", "platform", "account_id", name="uq_platform_account"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False, index=True)
    platform: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    account_id: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    url: Mapped[Optional[str]] = mapped_column(String(500))
    account_metadata: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)

    host: Mapped[Host] = relationship(back_populates="accounts")


class YouTubeChannelDaily(TimestampMixin, Base):
    __tablename__ = "youtube_channel_daily"
    __table_args__ = (UniqueConstraint("host_id", "day", name="uq_youtube_channel_daily"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False, index=True)
    day: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    subscribers: Mapped[Optional[int]] = mapped_column(Integer)
    videos_published: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    source_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class YouTubeVideoDaily(TimestampMixin, Base):
    __tablename__ = "youtube_video_daily"
    __table_args__ = (UniqueConstraint("host_id", "video_id", "day", name="uq_youtube_video_daily"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False, index=True)
    video_id: Mapped[str] = mapped_column(String(255), nullable=False)
    day: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    likes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comments: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    engagement_rate: Mapped[Optional[float]] = mapped_column(Float)
    source_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class GoogleTrendsDaily(TimestampMixin, Base):
    __tablename__ = "google_trends_daily"
    __table_args__ = (UniqueConstraint("host_id", "day", name="uq_google_trends_daily"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False, index=True)
    day: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    interest_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    source_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class SerpRankDaily(TimestampMixin, Base):
    __tablename__ = "serp_rank_daily"
    __table_args__ = (UniqueConstraint("host_id", "keyword", "day", name="uq_serp_rank_daily"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False, index=True)
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    day: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    average_rank: Mapped[float] = mapped_column(Float, nullable=False)
    best_rank: Mapped[Optional[int]] = mapped_column(Integer)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    source_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class PodcastMentionsDaily(TimestampMixin, Base):
    __tablename__ = "podcast_mentions_daily"
    __table_args__ = (UniqueConstraint("host_id", "episode_id", "day", name="uq_podcast_mentions_daily"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False, index=True)
    episode_id: Mapped[str] = mapped_column(String(255), nullable=False)
    day: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    podcast_name: Mapped[str] = mapped_column(String(255), nullable=False)
    episode_title: Mapped[str] = mapped_column(String(500), nullable=False)
    mention_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    source_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class SentimentDocument(TimestampMixin, Base):
    __tablename__ = "sentiment_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_document_id: Mapped[str] = mapped_column(String(255), nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    day: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    excerpt: Mapped[Optional[str]] = mapped_column(Text)
    sentiment_label: Mapped[Optional[str]] = mapped_column(String(30))
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    source_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class HostScoreDaily(TimestampMixin, Base):
    __tablename__ = "host_scores_daily"
    __table_args__ = (UniqueConstraint("host_id", "day", name="uq_host_scores_daily"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False, index=True)
    day: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    attention: Mapped[float] = mapped_column(Float, nullable=False)
    discoverability: Mapped[float] = mapped_column(Float, nullable=False)
    engagement: Mapped[float] = mapped_column(Float, nullable=False)
    sentiment: Mapped[float] = mapped_column(Float, nullable=False)
    crossover: Mapped[float] = mapped_column(Float, nullable=False)
    popularity_score: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    momentum_7d: Mapped[Optional[float]] = mapped_column(Float)
    momentum_30d: Mapped[Optional[float]] = mapped_column(Float)
    source_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class RawSourceEvent(TimestampMixin, Base):
    __tablename__ = "raw_source_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    cache_key: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    event_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    event_metadata: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)


class ProviderCacheEntry(TimestampMixin, Base):
    __tablename__ = "provider_cache_entries"
    __table_args__ = (UniqueConstraint("provider", "cache_key", name="uq_provider_cache_entry"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    cache_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    cache_metadata: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)
