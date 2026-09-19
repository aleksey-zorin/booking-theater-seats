"""Создание, отмена и проверка бронирований."""

from seats import is_seat_taken, seat_exists


def get_booking_status(is_available: bool) -> str:
    """Текстовый статус места (функция из ПР1)."""
    if is_available:
        return "Место доступно для бронирования"
    return "Место уже занято"


def is_seat_available(bookings: list[dict], show_id: int,
                      row: int, seat: int) -> bool:
    """Проверить, свободно ли место на данном показе."""
    return not is_seat_taken(bookings, show_id, row, seat)


def create_booking(bookings: list[dict], show: dict, row: int,
                   seat: int, viewer_name: str,
                   viewer_phone: str) -> dict:
    """Создать бронирование. Выбросить ValueError при конфликте."""
    if not seat_exists(show, row, seat):
        raise ValueError("Такого места в зале нет.")
    if is_seat_taken(bookings, show["show_id"], row, seat):
        raise ValueError("Место уже занято.")

    booking_id = (max((b["booking_id"] for b in bookings), default=0) + 1)
    booking = {
        "booking_id": booking_id,
        "show_id": show["show_id"],
        "row": row,
        "seat": seat,
        "viewer_name": viewer_name,
        "viewer_phone": viewer_phone,
    }
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[dict], booking_id: int) -> bool:
    """Отменить бронирование по идентификатору."""
    for i, booking in enumerate(bookings):
        if booking["booking_id"] == booking_id:
            bookings.pop(i)
            return True
    return False


def find_bookings_by_viewer(bookings: list[dict], query: str) -> list[dict]:
    """Найти бронирования по подстроке имени зрителя."""
    return [b for b in bookings if query.lower() in b["viewer_name"].lower()]
