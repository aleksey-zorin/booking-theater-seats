"""Веб-страницы бронирований."""

import sqlite3


from django.http import HttpResponse
from django.shortcuts import render

from storage import load_shows, load_users, load_bookings


def bookings_list(request) -> HttpResponse:
    """Страница /bookings/ — список броней."""
    shows = load_shows("data/shows.json")
    users = load_users("data/users.json")
    bookings = load_bookings("data/bookings.json", users, shows)

    context = {"bookings": bookings}
    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id: int) -> HttpResponse:
    """Страница /bookings/<booking_id>/ — карточка брони."""
    shows = load_shows("data/shows.json")
    users = load_users("data/users.json")
    bookings = load_bookings("data/bookings.json", users, shows)

    booking = next((b for b in bookings if b.id == booking_id), None)

    context = {"booking": booking}
    status = 200 if booking else 404
    return render(request, "bookings/booking_detail.html", context, status=status)


DB_PATH = "data/theatre.sqlite"


def statistics_sql(request) -> HttpResponse:
    """Статистика броней по спектаклям (JOIN + GROUP BY + HAVING)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    stats = conn.execute("""
        SELECT
            plays.title AS play_title,
            COUNT(bookings.id) AS bookings_count
        FROM plays
        LEFT JOIN shows ON shows.play_id = plays.id
        LEFT JOIN bookings ON bookings.show_id = shows.id
            AND bookings.is_cancelled = 0
        GROUP BY plays.id, plays.title
        ORDER BY bookings_count DESC
    """).fetchall()

    total = conn.execute(
        "SELECT COUNT(*) AS c FROM bookings WHERE is_cancelled = 0"
    ).fetchone()["c"]
    conn.close()

    context = {"statistics": stats, "total_active": total}
    return render(request, "bookings/statistics.html", context)
