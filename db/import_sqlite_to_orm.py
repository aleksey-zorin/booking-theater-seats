"""Перенос данных из data/theatre.sqlite в Django ORM (db.sqlite3)."""

import os
import sqlite3
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "theatre.settings")
django.setup()

from django.db import transaction  # noqa: E402

from bookings.models import Booking  # noqa: E402
from plays.models import Play, Show  # noqa: E402
from users.models import User  # noqa: E402

SOURCE_DB = BASE_DIR / "data" / "theatre.sqlite"


def main() -> None:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Нет файла {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row
        plays = conn.execute("SELECT * FROM plays").fetchall()
        shows = conn.execute("SELECT * FROM shows").fetchall()
        users = conn.execute("SELECT * FROM users").fetchall()
        bookings = conn.execute("SELECT * FROM bookings").fetchall()

    with transaction.atomic():
        for row in plays:
            Play.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "title": row["title"],
                    "genre": row["genre"],
                    "duration_min": row["duration_min"],
                },
            )
        for row in users:
            User.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "phone": row["phone"],
                    "email": row["email"] or "",
                },
            )
        for row in shows:
            Show.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "play_id": row["play_id"],
                    "datetime": row["datetime"],
                    "hall": row["hall"],
                    "rows": row["rows"],
                    "seats_per_row": row["seats_per_row"],
                },
            )
        for row in bookings:
            Booking.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "user_id": row["user_id"],
                    "show_id": row["show_id"],
                    "row": row["row"],
                    "seat": row["seat"],
                    "is_cancelled": bool(row["is_cancelled"]),
                },
            )

    print("Перенос завершён.")
    print(f"Спектаклей: {Play.objects.count()}")
    print(f"Показов:    {Show.objects.count()}")
    print(f"Зрителей:   {User.objects.count()}")
    print(f"Броней:     {Booking.objects.count()}")


if __name__ == "__main__":
    main()
