"""Веб-страницы спектаклей и показов."""

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
