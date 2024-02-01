from django.db import models

from mailing.models import MailingSettings

from customers.models import NULLABLE


class MailingLog(models.Model):
    '''Логи рассылки'''
    mailing = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, related_name='logs', verbose_name='Логи')
    timestamp = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=20, choices=[('success', 'Успешно'), ('failure', 'Ошибка')], verbose_name='Статус попытки')
    server_response = models.CharField(max_length=100, verbose_name='Ответ почтового сервера', **NULLABLE)

    def __str__(self):
        return f"Последняя попытка: {self.timestamp}, Статус: {self.status}, Ответ: {self.server_response}"

