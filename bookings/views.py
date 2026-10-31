"""Веб-страницы броней (ORM)."""

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from bookings.models import Booking
from plays.models import Play


def bookings_list(request):
    """Страница /bookings/ — список активных броней."""
    bookings = (
        Booking.objects
        .exclude(is_cancelled=False)
        .select_related("user", "show", "show__play")
        .order_by("-id")
    )
    return render(request, "bookings/booking_list.html", {"bookings": bookings})


def booking_detail(request, booking_id: int):
    """Страница /bookings/<booking_id>/ — карточка брони."""
    booking = get_object_or_404(
        Booking.objects.select_related("user", "show", "show__play"),
        pk=booking_id,
    )
    return render(request, "bookings/booking_detail.html", {"booking": booking})


def statistics_sql(request):
    """Страница /bookings/statistics/ — брони по спектаклям."""
    stats = (
        Play.objects
        .annotate(
            bookings_count=Count(
                "shows__bookings",
                filter=Q(shows__bookings__is_cancelled=False),
            )
        )
        .values("title", "bookings_count")
        .order_by("-bookings_count", "title")
    )
    total_active = Booking.objects.filter(is_cancelled=False).count()
    return render(
        request,
        "bookings/statistics.html",
        {"statistics": stats, "total_active": total_active},
    )
