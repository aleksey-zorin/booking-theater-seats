"""Маршруты приложения plays."""

from django.urls import path
from . import views

app_name = "plays"

urlpatterns = [
    path("", views.plays_list, name="list"),
    path("<int:play_id>/", views.play_detail, name="detail"),
    path("sql/", views.plays_list_sql, name="list_sql"),
    path("free-seats/", views.free_seats_sql, name="free_seats"),
]
