from django.contrib import admin

from .models import Ingredient, Recipe, Subscribe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display =('name', 'author','description', 'pub_date')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


# @admin.register(Unit)
# class UnitAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
#     list_filter = ('name',)
#     empty_value_display = '-пусто-'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('author',)
    list_filter = ('user', 'author',)
    empty_value_display = '-пусто-'



