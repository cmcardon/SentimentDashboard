from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.db.models import ProviderCacheEntry


class ProviderCache:
    def __init__(self, session: Session):
        self.session = session

    def get(self, provider: str, cache_key: str) -> Optional[dict[str, Any]]:
        entry = self.session.scalar(
            select(ProviderCacheEntry).where(
                ProviderCacheEntry.provider == provider,
                ProviderCacheEntry.cache_key == cache_key,
            )
        )
        now = datetime.now(timezone.utc)
        if entry is None or entry.expires_at < now:
            return None
        return entry.payload

    def set(
        self,
        provider: str,
        cache_key: str,
        payload: dict[str, Any],
        ttl_seconds: int,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        entry = self.session.scalar(
            select(ProviderCacheEntry).where(
                ProviderCacheEntry.provider == provider,
                ProviderCacheEntry.cache_key == cache_key,
            )
        )
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
        if entry is None:
            entry = ProviderCacheEntry(
                provider=provider,
                cache_key=cache_key,
                expires_at=expires_at,
                payload=payload,
                cache_metadata=metadata or {},
            )
            self.session.add(entry)
        else:
            entry.expires_at = expires_at
            entry.payload = payload
            entry.cache_metadata = metadata or {}
        self.session.commit()
