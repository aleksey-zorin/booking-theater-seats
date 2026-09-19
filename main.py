"""Точка входа приложения «Система бронирования мест в театре»."""

from plays import find_show, filter_plays_by_genre, \
    sort_plays_by_duration, show_play_info
from seats import free_seats_count
from bookings import (get_booking_status, is_seat_available,
                      create_booking, cancel_booking,
                      find_bookings_by_viewer)
from storage import load_json, save_json
from utils import input_int, input_non_empty

PLAYS_FILE = "data/plays.json"
BOOKINGS_FILE = "data/bookings.json"


def show_all_plays(plays: list[dict]) -> None:
    """Вывести все спектакли с показами."""
    if not plays:
        print("Список спектаклей пуст.")
        return
    for play in plays:
        show_play_info(play)


def show_bookings(bookings: list[dict], plays: list[dict]) -> None:
    """Вывести все бронирования."""
    if not bookings:
        print("Бронирований нет.")
        return
    for booking in bookings:
        show = find_show(plays, booking["show_id"])
        when = show["datetime"] if show else "?"
        print(f"[{booking['booking_id']}] показ {booking['show_id']} ({when}) "
              f"— ряд {booking['row']}, место {booking['seat']}, "
              f"зритель: {booking['viewer_name']}")


def menu() -> None:
    print("\n=== Система бронирования мест в театре ===")
    print("1. Показать спектакли")
    print("2. Фильтр по жанру")
    print("3. Сортировка по продолжительности")
    print("4. Свободных мест на показе")
    print("5. Проверить доступность места")
    print("6. Забронировать место")
    print("7. Отменить бронирование")
    print("8. Бронирования по зрителю")
    print("9. Показать все бронирования")
    print("0. Выход")


def main() -> None:
    """Основной цикл приложения."""
    plays = load_json(PLAYS_FILE)
    bookings = load_json(BOOKINGS_FILE)

    while True:
        menu()
        choice = input("Выберите действие: ").strip()

        if choice == "0":
            save_json(BOOKINGS_FILE, bookings)
            print("Данные сохранены. До встречи!")
            break

        if choice == "1":
            show_all_plays(plays)

        elif choice == "2":
            genre = input_non_empty("Жанр: ")
            for play in filter_plays_by_genre(plays, genre):
                show_play_info(play)

        elif choice == "3":
            for play in sort_plays_by_duration(plays):
                show_play_info(play)

        elif choice == "4":
            show_id = input_int("Идентификатор показа: ")
            show = find_show(plays, show_id)
            if show is None:
                print("Показ не найден.")
            else:
                print(f"Свободных мест: {free_seats_count(bookings, show)}")

        elif choice == "5":
            show_id = input_int("Идентификатор показа: ")
            row = input_int("Ряд: ")
            seat = input_int("Место: ")
            available = is_seat_available(bookings, show_id, row, seat)
            print(get_booking_status(available))

        elif choice == "6":
            show_id = input_int("Идентификатор показа: ")
            show = find_show(plays, show_id)
            if show is None:
                print("Показ не найден.")
                continue
            row = input_int("Ряд: ")
            seat = input_int("Место: ")
            name = input_non_empty("Имя зрителя: ")
            phone = input_non_empty("Телефон: ")
            try:
                booking = create_booking(bookings, show, row, seat,
                                         name, phone)
                save_json(BOOKINGS_FILE, bookings)
                print(f"Забронировано! Номер брони: {booking['booking_id']}")
            except ValueError as error:
                print(f"Не удалось забронировать: {error}")

        elif choice == "7":
            booking_id = input_int("Номер брони: ")
            if cancel_booking(bookings, booking_id):
                save_json(BOOKINGS_FILE, bookings)
                print("Бронь отменена.")
            else:
                print("Бронь не найдена.")

        elif choice == "8":
            query = input_non_empty("Часть имени зрителя: ")
            show_bookings(find_bookings_by_viewer(bookings, query), plays)

        elif choice == "9":
            show_bookings(bookings, plays)

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
