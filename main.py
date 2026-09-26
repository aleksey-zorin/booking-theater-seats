"""Точка входа: система бронирования мест в театре (ПР3, ООП)."""

from models import Play, Show, Seat, User, Booking
from models.plays import (
    find_show,
    filter_plays_by_genre,
    sort_plays_by_duration,
    show_play_info,
)
from models.seats import seat_exists, free_seats_count
from models.users import (
    add_user,
    find_user,
    find_user_by_id,
    show_users,
)
from models.bookings import (
    is_seat_available,
    create_booking,
    cancel_booking,
    find_bookings_by_user,
    show_bookings,
)
from storage import (
    load_plays, save_plays,
    load_shows, save_shows,
    load_users, save_users,
    load_bookings, save_bookings,
)
from utils import input_int, input_non_empty

PLAYS_FILE = "data/plays.json"
SHOWS_FILE = "data/shows.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


# --- Работа с показами в меню ---

def show_all_plays(plays: list[Play], shows: list[Show]) -> None:
    """Вывести все спектакли с их показами."""
    if not plays:
        print("Спектаклей нет.")
        return
    for play in plays:
        show_play_info(play, shows)


def show_shows(shows: list[Show]) -> None:
    """Вывести все показы."""
    if not shows:
        print("Показов нет.")
        return
    for show in shows:
        print(show)


# --- Добавление и поиск зрителей ---

def create_new_user(users: list[User]) -> None:
    """Запросить данные и добавить зрителя."""
    name = input_non_empty("Имя зрителя: ")
    phone = input_non_empty("Телефон: ")
    email = input("Email (можно пусто): ").strip()
    user = add_user(users, name, phone, email)
    save_users(USERS_FILE, users)
    print(f"Зритель добавлен: {user}")


def search_user(users: list[User]) -> None:
    """Найти зрителей по подстроке."""
    query = input_non_empty("Часть имени или телефона: ")
    found = find_user(users, query)
    if not found:
        print("Ничего не найдено.")
        return
    for user in found:
        print(user)


# --- Бронирование ---

def create_new_booking(bookings: list[Booking], shows: list[Show],
                       users: list[User]) -> None:
    """Сценарий создания брони с участием объектов User, Show, Seat."""
    if not shows:
        print("Нет доступных показов.")
        return
    if not users:
        print("Сначала добавьте хотя бы одного зрителя.")
        return

    show_id = input_int("Идентификатор показа: ")
    show = find_show(shows, show_id)
    if show is None:
        print("Показ не найден.")
        return

    user_id = input_int("Идентификатор зрителя: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("Зритель не найден.")
        return

    row = input_int("Ряд: ")
    seat_number = input_int("Место: ")

    if not seat_exists(show, row, seat_number):
        print("Такого места в зале нет.")
        return

    seat = Seat(show_id=show.id, row=row, number=seat_number)
    booking = create_booking(bookings, user, show, seat)
    if booking is None:
        print("Место уже занято на этот показ.")
        return

    save_bookings(BOOKINGS_FILE, bookings)
    print(f"Бронь создана: {booking}")


def cancel_existing_booking(bookings: list[Booking]) -> None:
    """Отменить бронь по идентификатору."""
    if not bookings:
        print("Бронирований нет.")
        return
    booking_id = input_int("Номер брони: ")
    if cancel_booking(bookings, booking_id):
        save_bookings(BOOKINGS_FILE, bookings)
        print("Бронь отменена.")
    else:
        print("Бронь не найдена.")


def search_bookings_by_user(bookings: list[Booking],
                            users: list[User]) -> None:
    """Показать брони конкретного зрителя."""
    if not users:
        print("Зрителей нет.")
        return
    user_id = input_int("Идентификатор зрителя: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("Зритель не найден.")
        return
    found = find_bookings_by_user(bookings, user)
    if not found:
        print("У зрителя нет броней.")
        return
    for booking in found:
        print(booking)


def check_seat_status(bookings: list[Booking], shows: list[Show]) -> None:
    """Проверить доступность конкретного места."""
    show_id = input_int("Идентификатор показа: ")
    show = find_show(shows, show_id)
    if show is None:
        print("Показ не найден.")
        return
    row = input_int("Ряд: ")
    seat_number = input_int("Место: ")
    if not seat_exists(show, row, seat_number):
        print("Такого места в зале нет.")
        return
    seat = Seat(show_id=show.id, row=row, number=seat_number)
    if is_seat_available(bookings, show, seat):
        print("Место доступно для бронирования")
    else:
        print("Место уже занято")


def show_free_seats(bookings: list[Booking], shows: list[Show]) -> None:
    """Показать число свободных мест на показе."""
    show_id = input_int("Идентификатор показа: ")
    show = find_show(shows, show_id)
    if show is None:
        print("Показ не найден.")
        return
    print(f"Свободных мест: {free_seats_count(bookings, show)}")


def search_plays(plays: list[Play], shows: list[Show]) -> None:
    """Фильтр спектаклей по жанру."""
    genre = input_non_empty("Жанр: ")
    found = filter_plays_by_genre(plays, genre)
    if not found:
        print("Ничего не найдено.")
        return
    for play in found:
        show_play_info(play, shows)


def sort_plays_menu(plays: list[Play], shows: list[Show]) -> None:
    """Сортировка спектаклей по продолжительности."""
    for play in sort_plays_by_duration(plays):
        show_play_info(play, shows)


# --- Меню ---

def menu() -> None:
    print("\n=== Система бронирования мест в театре ===")
    print("1.  Показать спектакли")
    print("2.  Фильтр спектаклей по жанру")
    print("3.  Сортировка спектаклей по продолжительности")
    print("4.  Показать показы")
    print("5.  Показать зрителей")
    print("6.  Добавить зрителя")
    print("7.  Найти зрителя")
    print("8.  Свободных мест на показе")
    print("9.  Проверить доступность места")
    print("10. Забронировать место")
    print("11. Отменить бронирование")
    print("12. Брони зрителя")
    print("13. Показать все бронирования")
    print("0.  Выход")


def main() -> None:
    """Загрузить данные, запустить меню, сохранить изменения."""
    plays = load_plays(PLAYS_FILE)
    shows = load_shows(SHOWS_FILE)
    users = load_users(USERS_FILE)
    bookings = load_bookings(BOOKINGS_FILE, users, shows)

    while True:
        menu()
        choice = input("Выберите действие: ").strip()

        if choice == "0":
            save_plays(PLAYS_FILE, plays)
            save_shows(SHOWS_FILE, shows)
            save_users(USERS_FILE, users)
            save_bookings(BOOKINGS_FILE, bookings)
            print("Данные сохранены. До встречи!")
            break

        elif choice == "1":
            show_all_plays(plays, shows)
        elif choice == "2":
            search_plays(plays, shows)
        elif choice == "3":
            sort_plays_menu(plays, shows)
        elif choice == "4":
            show_shows(shows)
        elif choice == "5":
            show_users(users)
        elif choice == "6":
            create_new_user(users)
        elif choice == "7":
            search_user(users)
        elif choice == "8":
            show_free_seats(bookings, shows)
        elif choice == "9":
            check_seat_status(bookings, shows)
        elif choice == "10":
            create_new_booking(bookings, shows, users)
        elif choice == "11":
            cancel_existing_booking(bookings)
        elif choice == "12":
            search_bookings_by_user(bookings, users)
        elif choice == "13":
            show_bookings(bookings)
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
