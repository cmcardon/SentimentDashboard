from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import select

from packages.db.models import Host, RawSourceEvent, YouTubeChannelDaily, YouTubeVideoDaily
from packages.db.session import SessionLocal
from packages.providers.mock import MockYouTubeProvider


def run(day: Optional[date] = None) -> None:
    target_day = day or date.today()
    provider = MockYouTubeProvider()
    with SessionLocal() as session:
        hosts = session.scalars(select(Host)).all()
        for host in hosts:
            result = provider.fetch_host_day(host.slug, target_day)
            payload = result.items[0]
            session.add(
                RawSourceEvent(
                    provider=result.provider,
                    source_type="youtube",
                    cache_key=f"{host.slug}:{target_day.isoformat()}",
                    event_at=datetime.now(timezone.utc),
                    payload=payload,
                    event_metadata={"host_slug": host.slug, "cache_hit": result.cache_hit},
                )
            )
            session.merge(
                YouTubeChannelDaily(
                    host_id=host.id,
                    day=target_day,
                    views=payload["channel_views"],
                    subscribers=payload["subscribers"],
                    videos_published=len(payload["videos"]),
                    source_metadata={"provider": result.provider},
                    raw_payload=payload,
                )
            )
            for video in payload["videos"]:
                session.merge(
                    YouTubeVideoDaily(
                        host_id=host.id,
                        video_id=video["id"],
                        day=target_day,
                        title=video["title"],
                        views=video["views"],
                        likes=video["likes"],
                        comments=video["comments"],
                        engagement_rate=round(((video["likes"] + video["comments"]) / max(video["views"], 1)) * 100, 2),
                        source_metadata={"provider": result.provider},
                        raw_payload=video,
                    )
                )
        session.commit()


if __name__ == "__main__":
    run()
