"""Django-модели спектаклей и показов."""

from django.db import models


class Play(models.Model):
    """Спектакль."""

    title = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    genre = models.CharField(
        max_length=100,
        verbose_name="Жанр",
    )
    duration_min = models.PositiveIntegerField(
        verbose_name="Продолжительность, мин.",
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Спектакль"
        verbose_name_plural = "Спектакли"

    def __str__(self) -> str:
        return self.title


class Show(models.Model):
    """Показ спектакля в зале."""

    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="shows",
        verbose_name="Спектакль",
    )
    datetime = models.CharField(
        max_length=50,
        verbose_name="Дата и время",
    )
    hall = models.CharField(
        max_length=100,
        verbose_name="Зал",
    )
    rows = models.PositiveIntegerField(verbose_name="Рядов")
    seats_per_row = models.PositiveIntegerField(
        verbose_name="Мест в ряду",
    )

    class Meta:
        ordering = ["datetime"]
        verbose_name = "Показ"
        verbose_name_plural = "Показы"

    def __str__(self) -> str:
        return f"{self.datetime} — {self.hall}"
