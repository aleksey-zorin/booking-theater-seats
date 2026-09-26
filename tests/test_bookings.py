"""Тесты бронирований."""

from models import Play, Show, Seat, User, Booking
from models.bookings import (
    is_seat_available,
    create_booking,
    cancel_booking,
    find_bookings_by_user,
)


def _make_env():
    play = Play(1, "Вишнёвый сад", "Драма", 150)
    show = Show(101, play.id, "20.09.2026 19:00",
                "Основной зал", 10, 12)
    user1 = User(1, "Иванов", "+7-900")
    user2 = User(2, "Петрова", "+7-901")
    return show, user1, user2


def test_booking_links_objects():
    show, user, _ = _make_env()
    seat = Seat(show.id, 5, 12)
    booking = Booking(1, user, show, seat)
    assert booking.user is user
    assert booking.show is show
    assert booking.seat.row == 5
    assert booking.seat.number == 12
    assert booking.is_cancelled is False


def test_booking_cancel():
    show, user, _ = _make_env()
    booking = Booking(1, user, show, Seat(show.id, 5, 12))
    booking.cancel()
    assert booking.is_cancelled is True


def test_create_booking_success():
    show, user, _ = _make_env()
    bookings: list[Booking] = []
    result = create_booking(bookings, user, show, Seat(show.id, 5, 12))
    assert result is not None
    assert len(bookings) == 1


def test_duplicate_booking_forbidden():
    show, user1, user2 = _make_env()
    bookings: list[Booking] = []
    create_booking(bookings, user1, show, Seat(show.id, 5, 12))
    result = create_booking(bookings, user2, show, Seat(show.id, 5, 12))
    assert result is None
    assert len(bookings) == 1


def test_cancelled_booking_frees_seat():
    show, user1, user2 = _make_env()
    bookings: list[Booking] = []
    b1 = create_booking(bookings, user1, show, Seat(show.id, 5, 12))
    b1.cancel()
    assert is_seat_available(bookings, show, Seat(show.id, 5, 12))
    b2 = create_booking(bookings, user2, show, Seat(show.id, 5, 12))
    assert b2 is not None


def test_cancel_booking_by_id():
    show, user, _ = _make_env()
    bookings: list[Booking] = []
    b = create_booking(bookings, user, show, Seat(show.id, 5, 12))
    assert cancel_booking(bookings, b.id) is True
    assert b.is_cancelled is True
    assert cancel_booking(bookings, 999) is False


def test_find_bookings_by_user():
    show, user1, user2 = _make_env()
    bookings: list[Booking] = []
    create_booking(bookings, user1, show, Seat(show.id, 1, 1))
    create_booking(bookings, user2, show, Seat(show.id, 1, 2))
    assert len(find_bookings_by_user(bookings, user1)) == 1
    assert len(find_bookings_by_user(bookings, user2)) == 1
