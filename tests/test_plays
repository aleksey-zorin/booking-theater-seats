"""Тесты спектаклей и показов."""

from models import Play, Show
from models.plays import (
    find_play,
    find_show,
    filter_plays_by_genre,
    sort_plays_by_duration,
)


def test_play_creation():
    play = Play(1, "Вишнёвый сад", "Драма", 150)
    assert play.id == 1
    assert play.title == "Вишнёвый сад"
    assert play.genre == "Драма"
    assert play.duration_min == 150


def test_show_creation():
    show = Show(101, 1, "20.09.2026 19:00", "Основной зал", 10, 12)
    assert show.id == 101
    assert show.play_id == 1
    assert show.rows == 10
    assert show.seats_per_row == 12


def test_find_play():
    plays = [Play(1, "Вишнёвый сад", "Драма", 150),
             Play(2, "Чайка", "Драма", 140)]
    assert find_play(plays, 2).title == "Чайка"
    assert find_play(plays, 99) is None


def test_find_show():
    shows = [Show(101, 1, "20.09.2026 19:00", "Основной зал", 10, 12)]
    assert find_show(shows, 101).play_id == 1
    assert find_show(shows, 999) is None


def test_filter_by_genre():
    plays = [Play(1, "Вишнёвый сад", "Драма", 150),
             Play(2, "Смешные люди", "Комедия", 100)]
    result = filter_plays_by_genre(plays, "драма")
    assert len(result) == 1
    assert result[0].title == "Вишнёвый сад"


def test_sort_by_duration():
    plays = [Play(1, "Длинный", "Драма", 200),
             Play(2, "Короткий", "Комедия", 60)]
    result = sort_plays_by_duration(plays)
    assert result[0].title == "Короткий"
    assert result[1].title == "Длинный"
