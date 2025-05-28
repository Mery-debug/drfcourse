from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


class Habits(models.Model):
    """Модель привычки"""
    PERIODICITY_CHOICES = [
        (1, "ежедневно"),
        (2, "через день"),
        (3, "раз в 3 дня"),
        (4, "раз в 4 дня"),
        (5, "раз в 5 дней"),
        (6, "раз в 6 дней"),
        (7, "еженедельно")
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    place = models.CharField(max_length=150, null=True, verbose_name="Место для выполнения привычки")
    time = models.TimeField(null=True, verbose_name="желаемое время", help_text="введите время в формате чч:мм")
    move = models.CharField(max_length=150, verbose_name="Привычка")
    good_hab = models.BooleanField(default=False, help_text="Признак приятной привычки")
    linked_hab = models.ForeignKey("self", on_delete=models.CASCADE, null=True, verbose_name="Связанная привычка")
    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(7)
        ],
        help_text="Периодичность выполнения: 1-ежедневно, а 7-еженедельно"
    )
    reward = models.TextField(verbose_name="Вознаграждение за выполнение привычки")
    execution_time = models.DurationField(
        verbose_name="Время на выполнение",
        help_text="Формат: ЧЧ:ММ:СС (например, 00:02:00 — 2 минуты)",
        validators=[
            MaxValueValidator(limit_value=timedelta(minutes=2))
        ],
        null=True,
        blank=True
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности"
    )
    last_remember = models.DateTimeField()

    def clean(self):
        """Валидация заданных полей привычки"""
        if self.good_hab and (self.reward or self.linked_hab):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку!")
        if not self.good_hab and self.reward and self.linked_hab:
            raise ValidationError("Укажите либо вознаграждение, либо связанную привычку!")

    @property
    def is_visible(self):
        """Проверка видимости привычки для любого пользователя"""
        return self.is_public

    def __str__(self):
        return f"{self.owner}, {self.move}"

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"




