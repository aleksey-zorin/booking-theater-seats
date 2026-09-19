"""Работа со спектаклями и показами."""

from typing import Optional


def find_play(plays: list[dict], play_id: int) -> Optional[dict]:
    """Найти спектакль по идентификатору. Вернуть None, если не найден."""
    for play in plays:
        if play["play_id"] == play_id:
            return play
    return None


def find_show(plays: list[dict], show_id: int) -> Optional[dict]:
    """Найти показ по идентификатору среди всех спектаклей."""
    for play in plays:
        for show in play["shows"]:
            if show["show_id"] == show_id:
                return show
    return None


def filter_plays_by_genre(plays: list[dict], genre: str) -> list[dict]:
    """Вернуть спектакли выбранного жанра."""
    return [play for play in plays if play["genre"].lower() == genre.lower()]


def sort_plays_by_duration(plays: list[dict]) -> list[dict]:
    """Вернуть спектакли, отсортированные по продолжительности."""
    return sorted(plays, key=lambda play: play["duration_min"])


def show_play_info(play: dict) -> None:
    """Вывести информацию о спектакле и его показах."""
    print(f"\n[{play['play_id']}] {play['title']} ({play['genre']}, "
          f"{play['duration_min']} мин.)")
    for show in play["shows"]:
        print(f"    показ {show['show_id']}: {show['datetime']}, "
              f"{show['hall']}")
