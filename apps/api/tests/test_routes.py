from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from apps.api.app.main import app
from packages.db.base import Base
from packages.db.seed import seed_hosts, seed_mock_metrics
from packages.db.session import get_db


def build_test_client() -> TestClient:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session:
        seed_hosts(session)
        seed_mock_metrics(session, lookback_days=35)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_leaderboard_route_returns_seeded_rows():
    client = build_test_client()
    response = client.get("/api/leaderboard")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 3
    assert "host_slug" in payload[0]


def test_host_detail_route_returns_detail_payload():
    client = build_test_client()
    leaderboard = client.get("/api/leaderboard").json()
    slug = leaderboard[0]["host_slug"]
    response = client.get(f"/api/hosts/{slug}")
    assert response.status_code == 200
    payload = response.json()
    assert payload["host_slug"] == slug
    assert len(payload["score_series"]) > 0
