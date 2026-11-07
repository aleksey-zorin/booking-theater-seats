"""Админ-панель приложения plays."""

from django.contrib import admin

from .models import Play, Show


class BookingInlineForShow(admin.TabularInline):
    """Брони, связанные с показом (в карточке показа)."""

    # Ссылка на модель строкой — защищает от циклического импорта,
    # потому что bookings.models импортирует plays.models (через Show).
    model = Show.bookings.rel.related_model
    fk_name = "show"
    fields = ("user", "row", "seat", "is_cancelled")
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ("user", "row", "seat")


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "genre", "duration_min")
    list_display_links = ("title",)
    search_fields = ("title", "genre")
    list_filter = ("genre",)
    ordering = ("title",)
    list_per_page = 20


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ("id", "play", "datetime", "hall", "rows", "seats_per_row")
    list_display_links = ("id",)
    search_fields = ("play__title", "hall")
    list_filter = ("hall", "play")
    ordering = ("datetime",)
    list_per_page = 20
    list_select_related = ("play",)
    inlines = (BookingInlineForShow,)
