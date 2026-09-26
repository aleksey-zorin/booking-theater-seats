"""Бронирования: связывают User + Show + Seat."""

from .plays import Show
from .seats import Seat
from .users import User


class Booking:
    """Бронирование места на показ зрителем."""

    def __init__(self, booking_id: int, user: User,
                 show: Show, seat: Seat) -> None:
        self.id = booking_id
        self.user = user
        self.show = show
        self.seat = seat
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить бронирование, не удаляя объект."""
        self.is_cancelled = True

    def __str__(self) -> str:
        status = "ОТМЕНЕНО" if self.is_cancelled else "активно"
        return (f"Бронь {self.id} [{status}]: {self.show.datetime}, "
                f"{self.seat}, зритель: {self.user.name}")


def is_seat_available(bookings: list[Booking],
                      show: Show, seat: Seat) -> bool:
    """Свободно ли место на показе (с учётом отмен)."""
    for booking in bookings:
        if booking.is_cancelled:
            continue
        if booking.show.id == show.id and booking.seat.is_same(seat):
            return False
    return True


def create_booking(bookings: list[Booking], user: User,
                   show: Show, seat: Seat) -> Booking | None:
    """Создать бронь. None, если место занято."""
    if not is_seat_available(bookings, show, seat):
        return None
    new_id = max((b.id for b in bookings), default=0) + 1
    booking = Booking(new_id, user, show, seat)
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[Booking], booking_id: int) -> bool:
    """Отменить бронь по идентификатору."""
    for booking in bookings:
        if booking.id == booking_id:
            booking.cancel()
            return True
    return False


def find_bookings_by_user(bookings: list[Booking],
                          user: User) -> list[Booking]:
    """Все брони указанного зрителя."""
    return [b for b in bookings if b.user.id == user.id]


def show_bookings(bookings: list[Booking]) -> None:
    """Вывести список броней."""
    if not bookings:
        print("Бронирований нет.")
        return
    for booking in bookings:
        print(booking)
