"""Маршруты приложения plays."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.plays_list, name="plays_list"),
    path("<int:play_id>/", views.play_detail, name="play_detail"),
]
