"""Админ-панель приложения users."""

from django.contrib import admin

from .models import User


class BookingInlineForUser(admin.TabularInline):
    """Брони, связанные со зрителем (в карточке зрителя)."""

    model = User.bookings.rel.related_model
    fk_name = "user"
    fields = ("show", "row", "seat", "is_cancelled")
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ("show", "row", "seat")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email")
    list_display_links = ("name",)
    search_fields = ("name", "phone", "email")
    ordering = ("name",)
    list_per_page = 20
    inlines = (BookingInlineForUser,)
