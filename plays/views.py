"""Веб-страницы спектаклей и показов (ORM)."""

from django.shortcuts import get_object_or_404, render

from bookings.models import Booking
from plays.models import Play, Show


def plays_list(request):
    """Страница /plays/ — список спектаклей через ORM."""
    plays = Play.objects.order_by("title")
    return render(request, "plays/play_list.html", {"plays": plays})


def play_detail(request, play_id: int):
    """Страница /plays/<play_id>/ — карточка спектакля с показами."""
    play = get_object_or_404(Play, pk=play_id)
    shows = play.shows.order_by("datetime")
    return render(
        request,
        "plays/play_detail.html",
        {"play": play, "shows": shows},
    )


def free_seats_sql(request):
    """Страница /plays/free-seats/ — занятые места на показе."""
    show_id = request.GET.get("show_id")
    seats = Booking.objects.none()
    error = None
    show = None

    if show_id:
        try:
            show_pk = int(show_id)
        except ValueError:
            error = "Некорректный идентификатор показа."
        else:
            show = Show.objects.filter(pk=show_pk).first()
            if show is None:
                error = "Показ не найден."
            else:
                seats = (
                    Booking.objects
                    .filter(show=show, is_cancelled=False)
                    .order_by("row", "seat")
                )

    return render(
        request,
        "plays/free_seats.html",
        {
            "show_id": show_id,
            "seats": seats,
            "error": error,
            "show": show,
        },
    )
