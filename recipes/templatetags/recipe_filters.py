from django import template

import pymorphy2
from recipes.models import FavoriteRecipe, Purchase, Recipe, Subscribe

morph = pymorphy2.MorphAnalyzer()

register = template.Library()


@register.filter()
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def get_tag_filter(value):
    return value.getlist('filters')


@register.filter
def get_filter_link(request, tag):
    new_request = request.GET.copy()
    page = new_request.get('page', None)

    if tag.title in request.GET.getlist('filters'):
        tags = new_request.getlist('filters')
        tags.remove(tag.title)
        new_request.setlist('filters', tags)
    else:
        new_request.appendlist('filters', tag.title)
    if page:
        new_request.pop('page')

    return new_request.urlencode()


@register.filter
def is_favorite(recipe, user):
    """Проверяет, что рецепт находится в 'Избранном'"""
    return FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def is_subscribe(user, author):
    """Проверяет, что пользователь подписан на автора'"""
    return Subscribe.objects.filter(user=user, author=author).exists()


@register.filter
def in_shoplist(recipe, user):
    """Проверяет, что рецепт находится в списке покупок"""
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag
def declension(count, word):
    """Склоняет слова"""
    zero_word = morph.parse(word)[0]
    return zero_word.make_agree_with_number(count).word


@register.simple_tag
def purchase_count(user):
    """Счётчик покупок"""
    return Recipe.objects.purchases(user=user).count()
