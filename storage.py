"""Загрузка и сохранение данных (JSON ↔ объекты)."""

import json
import os

from models import Play, Show, User, Booking
from models.seats import Seat


def _read_json(filename: str) -> list:
    """Прочитать JSON-файл. При отсутствии файла вернуть пустой список."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка чтения {filename}: {error}")
        return []


def _write_json(filename: str, data: list) -> None:
    """Записать данные в JSON-файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка записи {filename}: {error}")


# --- Спектакли ---

def load_plays(filename: str) -> list[Play]:
    """Загрузить спектакли из JSON."""
    return [Play(d["id"], d["title"], d["genre"], d["duration_min"])
            for d in _read_json(filename)]


def save_plays(filename: str, plays: list[Play]) -> None:
    """Сохранить спектакли в JSON."""
    data = [{"id": p.id, "title": p.title,
             "genre": p.genre, "duration_min": p.duration_min}
            for p in plays]
    _write_json(filename, data)


# --- Показы ---

def load_shows(filename: str) -> list[Show]:
    """Загрузить показы из JSON."""
    return [Show(d["id"], d["play_id"], d["datetime"], d["hall"],
                 d["rows"], d["seats_per_row"])
            for d in _read_json(filename)]


def save_shows(filename: str, shows: list[Show]) -> None:
    """Сохранить показы в JSON."""
    data = [{"id": s.id, "play_id": s.play_id, "datetime": s.datetime,
             "hall": s.hall, "rows": s.rows,
             "seats_per_row": s.seats_per_row}
            for s in shows]
    _write_json(filename, data)


# --- Зрители ---

def load_users(filename: str) -> list[User]:
    """Загрузить зрителей из JSON."""
    return [User.from_data(d) for d in _read_json(filename)]


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить зрителей в JSON."""
    _write_json(filename, [u.to_data() for u in users])


# --- Бронирования ---

def load_bookings(filename: str, users: list[User],
                  shows: list[Show]) -> list[Booking]:
    """JSON → объекты Booking со ссылками на User и Show."""
    bookings: list[Booking] = []
    for d in _read_json(filename):
        user = next((u for u in users if u.id == d["user_id"]), None)
        show = next((s for s in shows if s.id == d["show_id"]), None)
        if user is None or show is None:
            continue
        seat = Seat(show_id=show.id, row=d["row"], number=d["seat"])
        booking = Booking(d["id"], user, show, seat)
        booking.is_cancelled = d.get("is_cancelled", False)
        bookings.append(booking)
    return bookings


def save_bookings(filename: str, bookings: list[Booking]) -> None:
    """Объекты Booking → JSON с идентификаторами."""
    data = [{
        "id": b.id,
        "user_id": b.user.id,
        "show_id": b.show.id,
        "row": b.seat.row,
        "seat": b.seat.number,
        "is_cancelled": b.is_cancelled,
    } for b in bookings]
    _write_json(filename, data)
