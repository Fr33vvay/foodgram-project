from django import template

import pymorphy2
from recipes.models import FavoriteRecipe

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

    if tag.title in request.GET.getlist('filters'):
        tags = new_request.getlist('filters')
        tags.remove(tag.title)
        new_request.setlist('filters', tags)
    else:
        new_request.appendlist('filters', tag.title)

    return new_request.urlencode()


@register.filter
def is_favorite(recipe, user):
    """Проверяет, что рецепт находится в 'Избранном'"""
    return FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag
def declension(count, word):
    """Склоняет слова"""
    zero_word = morph.parse(word)[0]
    return zero_word.make_agree_with_number(count).word
