from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import select

from packages.db.models import GoogleTrendsDaily, Host, RawSourceEvent
from packages.db.session import SessionLocal
from packages.providers.mock import MockGoogleTrendsProvider


def run(day: Optional[date] = None) -> None:
    target_day = day or date.today()
    provider = MockGoogleTrendsProvider()
    with SessionLocal() as session:
        hosts = session.scalars(select(Host)).all()
        for host in hosts:
            result = provider.fetch_host_day(host.slug, target_day)
            payload = result.items[0]
            session.add(
                RawSourceEvent(
                    provider=result.provider,
                    source_type="google_trends",
                    cache_key=f"{host.slug}:{target_day.isoformat()}",
                    event_at=datetime.now(timezone.utc),
                    payload=payload,
                    event_metadata={"host_slug": host.slug},
                )
            )
            session.merge(
                GoogleTrendsDaily(
                    host_id=host.id,
                    day=target_day,
                    interest_score=payload["interest_score"],
                    source_metadata={"provider": result.provider},
                    raw_payload=payload,
                )
            )
        session.commit()


if __name__ == "__main__":
    run()
