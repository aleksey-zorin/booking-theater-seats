"""Спектакли и показы."""


class Play:
    """Спектакль."""

    def __init__(self, play_id: int, title: str,
                 genre: str, duration_min: int) -> None:
        self.id = play_id
        self.title = title
        self.genre = genre
        self.duration_min = duration_min

    def __str__(self) -> str:
        return (f"[{self.id}] {self.title} "
                f"({self.genre}, {self.duration_min} мин.)")


class Show:
    """Показ спектакля в зале."""

    def __init__(self, show_id: int, play_id: int, datetime_str: str,
                 hall: str, rows: int, seats_per_row: int) -> None:
        self.id = show_id
        self.play_id = play_id
        self.datetime = datetime_str
        self.hall = hall
        self.rows = rows
        self.seats_per_row = seats_per_row

    def __str__(self) -> str:
        return (f"Показ {self.id}: {self.datetime}, "
                f"{self.hall} ({self.rows}x{self.seats_per_row})")


def find_play(plays: list[Play], play_id: int) -> Play | None:
    """Найти спектакль по идентификатору."""
    for play in plays:
        if play.id == play_id:
            return play
    return None


def find_show(shows: list[Show], show_id: int) -> Show | None:
    """Найти показ по идентификатору."""
    for show in shows:
        if show.id == show_id:
            return show
    return None


def filter_plays_by_genre(plays: list[Play], genre: str) -> list[Play]:
    """Отобрать спектакли по жанру."""
    return [p for p in plays if p.genre.lower() == genre.lower()]


def sort_plays_by_duration(plays: list[Play]) -> list[Play]:
    """Отсортировать спектакли по продолжительности."""
    return sorted(plays, key=lambda p: p.duration_min)


def show_play_info(play: Play, shows: list[Show]) -> None:
    """Вывести спектакль и его показы."""
    print(play)
    for show in shows:
        if show.play_id == play.id:
            print(f"    {show}")
