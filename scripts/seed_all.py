from __future__ import annotations

from packages.db.seed import seed_hosts, seed_mock_metrics
from packages.db.session import SessionLocal


def main() -> None:
    with SessionLocal() as session:
        seed_hosts(session)
        seed_mock_metrics(session)
    print("Seeded hosts and mock metrics")


if __name__ == "__main__":
    main()

