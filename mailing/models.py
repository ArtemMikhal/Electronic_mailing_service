from django.db import models

from customers.models import Client


class MailingSettings(models.Model):
    '''Рассылка (настройки)'''
    TIME_CHOICES = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создано'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название рассылки', default='Без названия')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    send_time = models.TimeField(verbose_name='Время рассылки')
    frequency = models.CharField(max_length=20, choices=TIME_CHOICES, verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=20, verbose_name='Статус рассылки', default='Создано')
    is_active = models.BooleanField(default=False, verbose_name='Активность рассылки')
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active:
            self.status = 'В процессе'
        elif self.status != 'Создано':
            self.status = 'Завершено'
        super().save(*args, **kwargs)

