"""Django-модель бронирования."""

from django.db import models

from plays.models import Show
from users.models import User


class Booking(models.Model):
    """Бронирование места на показ."""

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Зритель",
    )
    show = models.ForeignKey(
        Show,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Показ",
    )
    row = models.PositiveIntegerField(verbose_name="Ряд")
    seat = models.PositiveIntegerField(verbose_name="Место")
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Отменено",
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self) -> str:
        return f"Бронь #{self.pk} — {self.show}"

    def cancel(self) -> None:
        """Отменить бронирование."""
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])
