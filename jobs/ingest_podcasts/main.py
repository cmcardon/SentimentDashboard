from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import select

from packages.db.models import Host, PodcastMentionsDaily, RawSourceEvent, SentimentDocument
from packages.db.session import SessionLocal
from packages.providers.mock import MockListenNotesProvider


def run(day: Optional[date] = None) -> None:
    target_day = day or date.today()
    provider = MockListenNotesProvider()
    with SessionLocal() as session:
        hosts = session.scalars(select(Host)).all()
        for host in hosts:
            result = provider.fetch_host_day(host.slug, target_day)
            for payload in result.items:
                session.add(
                    RawSourceEvent(
                        provider=result.provider,
                        source_type="podcasts",
                        cache_key=f"{host.slug}:{payload['episode_id']}",
                        event_at=datetime.now(timezone.utc),
                        payload=payload,
                        event_metadata={"host_slug": host.slug},
                    )
                )
                session.merge(
                    PodcastMentionsDaily(
                        host_id=host.id,
                        episode_id=payload["episode_id"],
                        day=target_day,
                        podcast_name=payload["podcast_name"],
                        episode_title=payload["episode_title"],
                        mention_count=payload["mention_count"],
                        confidence=payload["confidence"],
                        source_metadata={"provider": result.provider},
                        raw_payload=payload,
                    )
                )
                session.add(
                    SentimentDocument(
                        host_id=host.id,
                        source="podcasts",
                        source_document_id=payload["episode_id"],
                        published_at=datetime.now(timezone.utc),
                        day=target_day,
                        title=payload["episode_title"],
                        excerpt="Mock podcast mention for local development",
                        sentiment_label="neutral",
                        sentiment_score=0.1,
                        confidence=payload["confidence"],
                        source_metadata={"provider": result.provider},
                        raw_payload=payload,
                    )
                )
        session.commit()


if __name__ == "__main__":
    run()
