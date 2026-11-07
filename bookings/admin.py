"""Админ-панель приложения bookings."""

from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Настройки отображения броней в админ-панели."""

    list_display = ("id", "show", "user", "row", "seat", "is_cancelled")
    list_display_links = ("id",)
    search_fields = ("show__play__title", "user__name", "user__phone")
    list_filter = ("is_cancelled", "show__hall")
    ordering = ("-id",)
    list_per_page = 20
    list_select_related = ("user", "show", "show__play")

    # Поля только для чтения
    readonly_fields = ("id",)
