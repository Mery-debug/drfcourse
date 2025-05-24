from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Адрес почты")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return {self.email}

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
