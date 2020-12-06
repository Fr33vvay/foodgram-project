from django.contrib import admin

from .models import Amount, Ingredient, Recipe, Subscribe


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredient.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ('name', 'author', 'description', 'pub_date')
    search_fields = ('name', 'author', 'tag')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('author',)
    list_filter = ('user', 'author',)
    empty_value_display = '-пусто-'
