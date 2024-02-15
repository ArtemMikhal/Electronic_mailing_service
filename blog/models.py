from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to='blog_images', verbose_name='Изображение', **NULLABLE)
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title