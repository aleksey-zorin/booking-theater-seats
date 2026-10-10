"""Главная страница и своя страница 404."""

from django.http import HttpResponse
from django.shortcuts import render


def index(request) -> HttpResponse:
    """Главная страница проекта."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception) -> HttpResponse:
    """Своя страница 404."""
    return render(
        request,
        "homepage/page_not_found.html",
        status=404,
    )
