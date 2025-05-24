from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from drfcours.users.models import User


class Habits(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    place = models.CharField(max_length=150, null=True, verbose_name="Место для выполнения привычки")
    time = models.TimeField(null=True, verbose_name="желаемое время", help_text="введите время в формате чч:мм")
    move = models.CharField(max_length=150, verbose_name="Привычка")
    good_hab = models.BooleanField(default=False, help_text="Признак приятной привычки")
    linked_hab = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name="Связанная привычка")
    periodicity = models.IntegerField(
        verbose_name='Периодичность (в днях)',
        help_text="Введите число от 1 до 7, где 1 - ежедневное выполнение, а 7 - еженедельное",
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(7)
        ]
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

    def __str__(self):
        return f"{self.owner}, {self.move}"

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"



