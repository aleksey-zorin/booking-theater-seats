"""Сохранение и загрузка JSON-файлов."""

import json
import os


def load_json(filename: str) -> list:
    """Загрузить список из JSON-файла. Вернуть [] при отсутствии файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка чтения {filename}: {error}")
        return []


def save_json(filename: str, data: list) -> None:
    """Сохранить список в JSON-файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка записи {filename}: {error}")
