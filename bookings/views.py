
"""Веб-страницы бронирований."""

from django.http import HttpResponse

from homepage.views import page
from storage import load_shows, load_users, load_bookings


def bookings_list(request) -> HttpResponse:
    """Страница /bookings/ — список бронирований."""
    shows = load_shows("data/shows.json")
    users = load_users("data/users.json")
    bookings = load_bookings("data/bookings.json", users, shows)

    items = ""
    for booking in bookings:
        status = "отменено" if booking.is_cancelled else "активно"
        badge = "bg-secondary" if booking.is_cancelled else "bg-success"
        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <a href="/bookings/{booking.id}/">
                {booking.show.datetime} — место {booking.seat}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """

    content = f"""
    <h1>Бронирования</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Бронирования", content))


def booking_detail(request, booking_id: int) -> HttpResponse:
    """Страница /bookings/<booking_id>/ — карточка брони."""
    shows = load_shows("data/shows.json")
    users = load_users("data/users.json")
    bookings = load_bookings("data/bookings.json", users, shows)

    booking = next((b for b in bookings if b.id == booking_id), None)
    if booking is None:
        content = """
        <h1 class="text-danger">Бронирование не найдено</h1>
        <a href="/bookings/" class="btn btn-outline-secondary">
            ← к списку бронирований
        </a>
        """
        return HttpResponse(
            page("Бронирование не найдено", content),
            status=404,
        )

    status = "отменено" if booking.is_cancelled else "активно"
    badge = "bg-secondary" if booking.is_cancelled else "bg-success"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h1 class="card-title">Бронирование №{booking.id}</h1>
            <p class="card-text">
                <strong>Спектакль:</strong>
                {booking.show.datetime}<br>
                <strong>Место:</strong> {booking.seat}<br>
                <strong>Зритель:</strong> {booking.user.name}<br>
                <strong>Телефон:</strong> {booking.user.phone}<br>
                <strong>Статус:</strong>
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/bookings/" class="btn btn-outline-secondary">
                ← к списку бронирований
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Бронирование №{booking.id}", content))
