from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from api.models import Subscribe
from recipes.models import Amount, Ingredient, Recipe, Tag, FavoriteRecipe


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredient.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ('name', 'author', 'description', 'pub_date')
    search_fields = ('name', 'author', 'tag')
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


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('author',)
    list_filter = ('user', 'author',)
    empty_value_display = '-пусто-'


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'
