"""Работа с местами в зале."""


def seat_exists(show: dict, row: int, seat: int) -> bool:
    """Проверить, существует ли такое место в зале показа."""
    return 1 <= row <= show["rows"] and 1 <= seat <= show["seats_per_row"]


def is_seat_taken(bookings: list[dict], show_id: int,
                  row: int, seat: int) -> bool:
    """Проверить, занято ли место на данном показе."""
    for booking in bookings:
        if (booking["show_id"] == show_id
                and booking["row"] == row
                and booking["seat"] == seat):
            return True
    return False


def free_seats_count(bookings: list[dict], show: dict) -> int:
    """Вернуть число свободных мест на показе."""
    total = show["rows"] * show["seats_per_row"]
    taken = sum(1 for booking in bookings
                if booking["show_id"] == show["show_id"])
    return total - taken
