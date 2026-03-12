from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Protocol


@dataclass
class ProviderResult:
    provider: str
    items: list[dict[str, Any]]
    fetched_at: datetime
    cache_hit: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class ProviderAdapter(Protocol):
    provider_name: str

    def fetch_host_day(self, host_slug: str, day: date, **kwargs: Any) -> ProviderResult:
        ...


class SocialProviderAdapter(ProviderAdapter, Protocol):
    ...


class SearchProviderAdapter(ProviderAdapter, Protocol):
    ...


class PodcastProviderAdapter(ProviderAdapter, Protocol):
    ...
