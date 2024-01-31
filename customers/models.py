from django.db import models


NULLABLE = {'blank': True, 'null': True}

class Client(models.Model):
    client_email = models.EmailField(unique=True, verbose_name='Почта')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name} {self.middle_name}'
        else:
            return f'{self.last_name} {self.first_name}'

