"""Тесты работы с местами."""

from seats import seat_exists, is_seat_taken, free_seats_count

SHOW = {"show_id": 101, "rows": 10, "seats_per_row": 12, "datetime": "20.09.2026 19:00"}


def test_seat_exists_true():
    assert seat_exists(SHOW, 5, 12)


def test_seat_exists_false():
    assert not seat_exists(SHOW, 11, 1)


def test_is_seat_taken():
    bookings = [{"show_id": 101, "row": 5, "seat": 12,
                 "viewer_name": "Иванов", "viewer_phone": "+7"}]
    assert is_seat_taken(bookings, 101, 5, 12)
    assert not is_seat_taken(bookings, 101, 5, 11)


def test_free_seats_count():
    bookings = [{"show_id": 101, "row": 1, "seat": 1,
                 "viewer_name": "A", "viewer_phone": "+7"},
                {"show_id": 102, "row": 1, "seat": 1,
                 "viewer_name": "B", "viewer_phone": "+7"}]
    assert free_seats_count(bookings, SHOW) == 120 - 1
