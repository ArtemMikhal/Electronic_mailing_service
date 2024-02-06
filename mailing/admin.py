from django.contrib import admin

from mailing.models import MailingSettings

@admin.register(MailingSettings)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('send_time', 'frequency',)
    search_fields = ('frequency',)
    readonly_fields = ('status',)  # Указываем, что поле 'status' только для чтения

