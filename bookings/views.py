"""Веб-страницы бронирований."""

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
