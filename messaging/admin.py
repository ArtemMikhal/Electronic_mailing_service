from django.contrib import admin

from django.contrib import admin

from messaging.models import MailingMessage

#admin.site.register(MailingMessage)
@admin.register(MailingMessage)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('subject', 'mailing',)



