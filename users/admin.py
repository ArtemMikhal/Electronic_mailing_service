

from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_filter = ('groups',)  # Добавляем фильтр по полю 'groups'

admin.site.register(User, UserAdmin)
