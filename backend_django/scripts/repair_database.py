"""Repair and validate the local SQLite database.

This script is safe to run repeatedly. It specifically handles the failure mode
where Django's migration table says sessions/token_blacklist were applied while
their physical SQLite tables are missing.
"""
from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db.sqlite3"
MANAGE = ROOT / "manage.py"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_django.settings")

REQUIRED = {
    "sessions": {"django_session"},
    "token_blacklist": {
        "token_blacklist_outstandingtoken",
        "token_blacklist_blacklistedtoken",
    },
}


def tables() -> set[str]:
    if not DB.exists():
        return set()
    con = sqlite3.connect(DB)
    try:
        return {
            row[0]
            for row in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
    finally:
        con.close()


def migration_rows(app: str) -> list[str]:
    con = sqlite3.connect(DB)
    try:
        return [
            row[0]
            for row in con.execute(
                "SELECT name FROM django_migrations WHERE app=? ORDER BY name", (app,)
            )
        ]
    finally:
        con.close()


def remove_migration_records(app: str) -> None:
    if not DB.exists():
        return
    con = sqlite3.connect(DB)
    try:
        con.execute("DELETE FROM django_migrations WHERE app=?", (app,))
        con.commit()
    finally:
        con.close()


def run_manage(*args: str) -> None:
    cmd = [sys.executable, str(MANAGE), *args]
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    print(f"Database: {DB}")
    if not DB.exists():
        print("No SQLite database found; Django migrate will create it.")
        run_manage("migrate", "--noinput")
    else:
        current = tables()
        for app, required_tables in REQUIRED.items():
            missing = required_tables - current
            if missing:
                print(f"Missing {app} tables: {sorted(missing)}")
                if "django_migrations" in current:
                    print(f"Releasing migration records for {app} so Django can recreate them.")
                    remove_migration_records(app)
                run_manage("migrate", app, "--noinput")
                current = tables()

        # Always bring any new migrations up to date.
        run_manage("migrate", "--noinput")

    final_tables = tables()
    missing_all = {t for values in REQUIRED.values() for t in values} - final_tables
    if missing_all:
        raise SystemExit(f"Database repair failed; missing tables: {sorted(missing_all)}")

    if DB.exists():
        con = sqlite3.connect(DB)
        try:
            integrity = con.execute("PRAGMA integrity_check").fetchone()[0]
        finally:
            con.close()
        if integrity != "ok":
            raise SystemExit(f"SQLite integrity_check failed: {integrity}")

    print("Database repair/validation: PASS")
    print("Required tables: PASS")
    print("SQLite integrity: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
