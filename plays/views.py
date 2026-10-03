
"""Веб-страницы спектаклей и показов."""

from django.http import HttpResponse

from homepage.views import page
from storage import load_plays, load_shows


def plays_list(request) -> HttpResponse:
    """Страница /plays/ — список спектаклей."""
    plays = load_plays("data/plays.json")
    shows = load_shows("data/shows.json")

    items = ""
    for play in plays:
        play_shows = [s for s in shows if s.play_id == play.id]
        shows_count = len(play_shows)
        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <a href="/plays/{play.id}/">{play.title}</a>
            <span class="badge bg-secondary">{shows_count} показов</span>
        </li>
        """

    content = f"""
    <h1>Спектакли</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Спектакли", content))


def play_detail(request, play_id: int) -> HttpResponse:
    """Страница /plays/<play_id>/ — карточка спектакля с показами."""
    plays = load_plays("data/plays.json")
    shows = load_shows("data/shows.json")

    play = next((p for p in plays if p.id == play_id), None)
    if play is None:
        content = """
        <h1 class="text-danger">Спектакль не найден</h1>
        <a href="/plays/" class="btn btn-outline-secondary">
            ← к списку спектаклей
        </a>
        """
        return HttpResponse(
            page("Спектакль не найден", content),
            status=404,
        )

    play_shows = [s for s in shows if s.play_id == play.id]
    show_items = ""
    for show in play_shows:
        show_items += f"""
        <li class="list-group-item">
            <strong>{show.datetime}</strong> —
            {show.hall}, {show.rows}×{show.seats_per_row} мест
        </li>
        """

    content = f"""
    <div class="card">
        <div class="card-body">
            <h1 class="card-title">{play.title}</h1>
            <p class="card-text">
                <strong>Жанр:</strong> {play.genre}<br>
                <strong>Продолжительность:</strong> {play.duration_min} мин.
            </p>
            <h3>Показы</h3>
            <ul class="list-group">{show_items}</ul>
            <a href="/plays/" class="btn btn-outline-secondary mt-3">
                ← к списку спектаклей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(play.title, content))
