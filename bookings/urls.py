"""Маршруты приложения bookings."""

from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.bookings_list, name="list"),
    path("<int:booking_id>/", views.booking_detail, name="detail"),
]
