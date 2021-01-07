from django.contrib import admin
from users.models import Subscribe


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('author__username',)
    list_filter = ('user', 'author',)
    empty_value_display = '-пусто-'
