from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from recipes.models import (
    Amount,
    FavoriteRecipe,
    Ingredient,
    Purchase,
    Recipe,
    Tag
)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredient.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    def count_favorites(self, recipe):
        """Считает число добавлений рецепта в 'Избранное'"""
        return recipe.favorites.count()

    inlines = (IngredientInline,)
    list_display = ('name', 'author')
    search_fields = ('name',)
    readonly_fields = ('count_favorites', 'pub_date')
    list_filter = ('name', 'author', 'tag')
    empty_value_display = '-пусто-'
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
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


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('recipe__name',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('recipe__name',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'
