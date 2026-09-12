# Показ
play_title = "Вишнёвый сад"
play_genre = "Драма"
play_duration = 150
show_datetime = "20.09.2026 19:00"

# Зал
hall_name = "Основной зал"
hall_size = 120
seat_row = 5
seat_number = 12
seat_is_taken = True

# Зритель
viewer_name = "Иванов Иван"
viewer_phone = "+7-900-123-45-67"


def show_play_info():
    """Функция 1. Показывает информацию о спектакле и показе."""
    return (f"Спектакль: {play_title}\n"
            f"Жанр: {play_genre}\n"
            f"Продолжительность: {play_duration} мин.\n"
            f"Показ: {show_datetime}")


def show_seat_status():
    """Функция 2. Показывает состояние выбранного места в зале."""
    status = "занято" if seat_is_taken else "свободно"
    return (f"Зал: {hall_name} (всего мест: {hall_size})\n"
            f"Ряд {seat_row}, место {seat_number}: {status}")


def book_seat():
    """Функция 3. Бронирует выбранное место за зрителем."""
    if seat_is_taken:
        return "Бронирование невозможно: место уже занято."
    return (f"Место забронировано!\n"
            f"Зритель: {viewer_name}\n"
            f"Телефон: {viewer_phone}\n"
            f"Ряд {seat_row}, место {seat_number}")


# Вывод
print(show_play_info())
print("-" * 40)
print(show_seat_status())
print("-" * 40)
print(book_seat())