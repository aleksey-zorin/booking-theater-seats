"""Django-модель зрителя."""

from django.db import models


class User(models.Model):
    """Зритель."""

    name = models.CharField(max_length=200, verbose_name="Имя")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(
        blank=True,
        default="",
        verbose_name="Email",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Зритель"
        verbose_name_plural = "Зрители"

    def __str__(self) -> str:
        return self.name
