"""Место в зале."""


class Seat:
    """Место в зале: ряд и номер на конкретном показе."""

    def __init__(self, show_id: int, row: int, number: int) -> None:
        self.show_id = show_id
        self.row = row
        self.number = number

    def is_same(self, other: "Seat") -> bool:
        """Совпадает ли место (тот же показ, ряд, номер)."""
        return (self.show_id == other.show_id
                and self.row == other.row
                and self.number == other.number)

    def __str__(self) -> str:
        return f"ряд {self.row}, место {self.number}"


def seat_exists(show, row: int, number: int) -> bool:
    """Существует ли такое место в зале показа."""
    return 1 <= row <= show.rows and 1 <= number <= show.seats_per_row


def find_seat(seats: list[Seat], show_id: int,
              row: int, number: int) -> Seat | None:
    """Найти место в коллекции."""
    for seat in seats:
        if (seat.show_id == show_id
                and seat.row == row
                and seat.number == number):
            return seat
    return None


def free_seats_count(bookings: list, show) -> int:
    """Число свободных мест на показе."""
    total = show.rows * show.seats_per_row
    taken = sum(1 for b in bookings
                if b.show.id == show.id and not b.is_cancelled)
    return total - taken
