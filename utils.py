"""Вспомогательные функции безопасного ввода."""

from datetime import datetime


def input_int(prompt: str) -> int:
    """Запросить целое число, повторяя запрос при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_non_empty(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: строка не должна быть пустой.")


def input_datetime(prompt: str, fmt: str = "%d.%m.%Y %H:%M") -> str:
    """Запросить дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ."""
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, fmt)
            return value
        except ValueError:
            print(f"Ошибка: используйте формат {fmt}.")
