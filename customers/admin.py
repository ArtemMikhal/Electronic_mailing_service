from django.contrib import admin

from customers.models import Client

#admin.site.register(Client)
@admin.register(Client)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'client_email', )
    search_fields = ('last_name',)

