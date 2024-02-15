from django.contrib import admin

from blog.models import Blog

#admin.site.register(Blog)

@admin.register(Blog)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('publication_date', 'title', 'author', 'views')
    list_filter = ('views', 'publication_date')
    search_fields = ('title', 'author',)
    readonly_fields = ('views',)