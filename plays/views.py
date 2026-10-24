"""Веб-страницы спектаклей и показов."""
import sqlite3


from django.http import HttpResponse
from django.shortcuts import render

from storage import load_plays, load_shows


def plays_list(request) -> HttpResponse:
    """Страница /plays/ — список спектаклей."""
    plays = load_plays("data/plays.json")
    context = {"plays": plays}
    return render(request, "plays/play_list.html", context)


def play_detail(request, play_id: int) -> HttpResponse:
    """Страница /plays/<play_id>/ — карточка спектакля с показами."""
    plays = load_plays("data/plays.json")
    shows = load_shows("data/shows.json")

    play = next((p for p in plays if p.id == play_id), None)
    play_shows = [s for s in shows if play and s.play_id == play.id]

    context = {
        "play": play,
        "shows": play_shows,
    }
    status = 200 if play else 404
    return render(request, "plays/play_detail.html", context, status=status)


DB_PATH = "data/theatre.sqlite"


def plays_list_sql(request) -> HttpResponse:
    """Список спектаклей из SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    plays = conn.execute(
        "SELECT id, title, genre, duration_min FROM plays ORDER BY title"
    ).fetchall()
    conn.close()
    context = {"plays": plays}
    return render(request, "plays/play_list_sql.html", context)


def free_seats_sql(request) -> HttpResponse:
    """Показать свободные места на показе (WHERE + параметризованный запрос)."""
    show_id = request.GET.get("show_id")
    seats = []
    if show_id:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        seats = conn.execute(
            "SELECT row, seat FROM bookings "
            "WHERE show_id = ? AND is_cancelled = 0",
            [show_id],
        ).fetchall()
        conn.close()
    context = {"show_id": show_id, "seats": seats}
    return render(request, "plays/free_seats.html", context)
