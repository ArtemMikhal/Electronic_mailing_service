from django.contrib.auth import get_user_model
from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Client(models.Model):
    client_email = models.EmailField(unique=True, verbose_name='Почта')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', **NULLABLE)
    first_name = models.CharField(max_length=100, verbose_name='Имя', **NULLABLE)
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь создавший", **NULLABLE)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.client_email

