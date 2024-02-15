
from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    is_verified = models.BooleanField(default=False, verbose_name='подтвержден ли аккаунт')
    is_blocked = models.BooleanField(default=False, verbose_name='заблокирован ли аккаунт')
    verification_token = models.CharField(max_length=100, **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('block_service_users', 'Может блокировать пользователей сервиса'),
        ]