"""Тесты бронирований."""

import pytest

from bookings import (get_booking_status, is_seat_available,
                      create_booking, cancel_booking,
                      find_bookings_by_viewer)

SHOW = {"show_id": 101, "rows": 10, "seats_per_row": 12,
        "datetime": "20.09.2026 19:00"}


def test_status_text():
    assert "доступно" in get_booking_status(True).lower()
    assert "занято" in get_booking_status(False).lower()


def test_create_and_availability():
    bookings = []
    create_booking(bookings, SHOW, 5, 12, "Иванов Иван", "+7-900")
    assert not is_seat_available(bookings, 101, 5, 12)
    assert is_seat_available(bookings, 101, 5, 11)


def test_duplicate_booking_forbidden():
    bookings = []
    create_booking(bookings, SHOW, 5, 12, "Иванов Иван", "+7-900")
    with pytest.raises(ValueError):
        create_booking(bookings, SHOW, 5, 12, "Петров Пётр", "+7-901")


def test_invalid_seat():
    bookings = []
    with pytest.raises(ValueError):
        create_booking(bookings, SHOW, 99, 1, "Иванов", "+7")


def test_cancel_and_search_by_viewer():
    bookings = []
    booking = create_booking(bookings, SHOW, 1, 1, "Иванов Иван", "+7")
    assert find_bookings_by_viewer(bookings, "иван")
    assert cancel_booking(bookings, booking["booking_id"])
    assert not bookings
