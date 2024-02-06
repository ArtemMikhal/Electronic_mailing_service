from django.db import models

from customers.models import NULLABLE
from mailing.models import MailingSettings



class MailingMessage(models.Model):
    '''Cообщение для рассылки'''
    mailing = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


