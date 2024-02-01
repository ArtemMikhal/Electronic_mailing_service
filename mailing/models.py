from django.db import models

from customers.models import Client


class MailingSettings(models.Model):
    '''Рассылка (настройки)'''
    TIME_CHOICES = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    clients = models.ManyToManyField(Client, related_name='mailings', verbose_name='Клиенты')
    send_time = models.DateTimeField(auto_now=True, verbose_name='Дата и время рассылки')
    frequency = models.CharField(max_length=20, choices=TIME_CHOICES, verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=20,
                              choices=[('created', 'Создано'), ('in_progress', 'В процессе'), ('completed', 'Завершено')],
                              verbose_name='Статус рассылки')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"{self.get_frequency_display()} рассылка ({self.send_time})"

