from __future__ import annotations

from pathlib import Path

from sqlalchemy import text

from packages.db.session import engine


def main() -> None:
    migrations_dir = Path("migrations")
    with engine.begin() as connection:
        for path in sorted(migrations_dir.glob("*.sql")):
            sql = path.read_text(encoding="utf-8")
            connection.execute(text(sql))
            print(f"Applied {path.name}")


if __name__ == "__main__":
    main()
