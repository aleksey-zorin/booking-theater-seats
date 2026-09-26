"""Тесты мест."""

from models import Show, Seat
from models.seats import seat_exists, find_seat, free_seats_count


def _make_show():
    return Show(101, 1, "20.09.2026 19:00", "Основной зал", 10, 12)


def test_seat_creation():
    seat = Seat(show_id=101, row=5, number=12)
    assert seat.show_id == 101
    assert seat.row == 5
    assert seat.number == 12


def test_seat_is_same():
    a = Seat(101, 5, 12)
    b = Seat(101, 5, 12)
    c = Seat(101, 5, 11)
    assert a.is_same(b)
    assert not a.is_same(c)


def test_seat_exists():
    show = _make_show()
    assert seat_exists(show, 5, 12)
    assert not seat_exists(show, 11, 1)
    assert not seat_exists(show, 0, 1)


def test_find_seat():
    seats = [Seat(101, 5, 12), Seat(101, 6, 3)]
    assert find_seat(seats, 101, 5, 12).row == 5
    assert find_seat(seats, 101, 7, 1) is None


def test_free_seats_count():
    show = _make_show()

    class _BookingStub:
        def __init__(self, show, cancelled=False):
            self.show = show
            self.is_cancelled = cancelled

    bookings = [
        _BookingStub(show, cancelled=False),
        _BookingStub(show, cancelled=True),
    ]
    # 10*12 = 120, одно активное бронирование → 119
    assert free_seats_count(bookings, show) == 119
