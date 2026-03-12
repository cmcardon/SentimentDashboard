from __future__ import annotations

from packages.db.seed import seed_mock_metrics
from packages.db.session import SessionLocal


def run() -> None:
    with SessionLocal() as session:
        seed_mock_metrics(session)


if __name__ == "__main__":
    run()

