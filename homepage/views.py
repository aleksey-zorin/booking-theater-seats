
"""Главная страница и общий каркас HTML для всех страниц проекта."""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Собрать HTML-документ с общим каркасом.

    :param title: заголовок вкладки браузера
    :param content: HTML-содержимое страницы
    :return: готовая HTML-строка
    """
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Театр</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/plays/">Спектакли</a>
                <a class="nav-link" href="/bookings/">Бронирования</a>
            </div>
        </div>
    </nav>
    <main class="container">
        {content}
    </main>
</body>
</html>"""


def index(request) -> HttpResponse:
    """Главная страница проекта."""
    content = """
    <h1 class="display-4">Система бронирования мест в театре</h1>
    <p class="lead">Просмотр спектаклей, показов и бронирований.</p>
    <p>Основные разделы:</p>
    <a href="/plays/" class="btn btn-primary me-2">Спектакли</a>
    <a href="/bookings/" class="btn btn-secondary">Бронирования</a>
    """
    return HttpResponse(page("Театр — главная", content))
