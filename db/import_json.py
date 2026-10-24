"""Перенос данных из JSON-файлов в SQLite."""

import json

from db.database import get_connection

PLAYS_FILE = "data/plays.json"
SHOWS_FILE = "data/shows.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def load_json(filename: str) -> list:
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def import_plays(conn) -> None:
    plays = load_json(PLAYS_FILE)
    conn.executemany(
        "INSERT INTO plays (id, title, genre, duration_min) "
        "VALUES (?, ?, ?, ?)",
        [(p["id"], p["title"], p["genre"], p["duration_min"])
         for p in plays],
    )


def import_shows(conn) -> None:
    shows = load_json(SHOWS_FILE)
    conn.executemany(
        "INSERT INTO shows (id, play_id, datetime, hall, rows, "
        "seats_per_row) VALUES (?, ?, ?, ?, ?, ?)",
        [(s["id"], s["play_id"], s["datetime"], s["hall"],
          s["rows"], s["seats_per_row"])
         for s in shows],
    )


def import_users(conn) -> None:
    users = load_json(USERS_FILE)
    conn.executemany(
        "INSERT INTO users (id, name, phone, email) "
        "VALUES (?, ?, ?, ?)",
        [(u["id"], u["name"], u["phone"], u.get("email", ""))
         for u in users],
    )


def import_bookings(conn) -> None:
    bookings = load_json(BOOKINGS_FILE)
    conn.executemany(
        "INSERT INTO bookings (id, user_id, show_id, row, seat, "
        "is_cancelled) VALUES (?, ?, ?, ?, ?, ?)",
        [(b["id"], b["user_id"], b["show_id"], b["row"], b["seat"],
          int(b.get("is_cancelled", False)))
         for b in bookings],
    )


def main() -> None:
    conn = get_connection()
    try:
        import_plays(conn)
        import_shows(conn)
        import_users(conn)
        import_bookings(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
