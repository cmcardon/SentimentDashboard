from __future__ import annotations

from datetime import date, datetime, timezone

from packages.providers.base import ProviderResult


class MockYouTubeProvider:
    provider_name = "mock_youtube"

    def fetch_host_day(self, host_slug: str, day: date, **kwargs):
        base = len(host_slug) * 1000 + day.day * 125
        return ProviderResult(
            provider=self.provider_name,
            fetched_at=datetime.now(timezone.utc),
            items=[
                {
                    "channel_views": 12000 + base,
                    "subscribers": 100000 + base,
                    "videos": [
                        {
                            "id": f"{host_slug}-{day.isoformat()}",
                            "title": f"{host_slug} show clip",
                            "views": 4000 + base // 2,
                            "likes": 200 + day.day,
                            "comments": 40 + day.day,
                        }
                    ],
                }
            ],
        )


class MockGoogleTrendsProvider:
    provider_name = "mock_google_trends"

    def fetch_host_day(self, host_slug: str, day: date, **kwargs):
        return ProviderResult(
            provider=self.provider_name,
            fetched_at=datetime.now(timezone.utc),
            items=[{"interest_score": min(100, 35 + len(host_slug) + day.day)}],
        )


class MockSerpProvider:
    provider_name = "mock_serp"

    def fetch_host_day(self, host_slug: str, day: date, **kwargs):
        return ProviderResult(
            provider=self.provider_name,
            fetched_at=datetime.now(timezone.utc),
            items=[{"keyword": host_slug.replace("-", " "), "average_rank": max(1, 12 - (day.day % 5)), "best_rank": 1}],
        )


class MockListenNotesProvider:
    provider_name = "mock_listen_notes"

    def fetch_host_day(self, host_slug: str, day: date, **kwargs):
        return ProviderResult(
            provider=self.provider_name,
            fetched_at=datetime.now(timezone.utc),
            items=[
                {
                    "episode_id": f"{host_slug}-{day.isoformat()}",
                    "podcast_name": "Mock Podcast",
                    "episode_title": f"{host_slug} appearance",
                    "mention_count": 2 + (day.day % 3),
                    "confidence": 0.86,
                }
            ],
        )


class StubXProvider:
    provider_name = "stub_x"

    def fetch_host_day(self, host_slug: str, day: date, **kwargs):
        return ProviderResult(provider=self.provider_name, fetched_at=datetime.now(timezone.utc), items=[])


class StubNewsProvider:
    provider_name = "stub_news"

    def fetch_host_day(self, host_slug: str, day: date, **kwargs):
        return ProviderResult(provider=self.provider_name, fetched_at=datetime.now(timezone.utc), items=[])

