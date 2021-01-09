from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from foodgram.settings import ITEMS
from recipes.forms import RecipeForm
from recipes.models import Amount, Purchase, Recipe, Subscribe, User
from recipes.utils import (
    get_ingredients,
    get_recipes_by_tags,
    recipe_form_save,
    shopping_list
)


def index(request):
    """Предоставляет список рецептов для всех пользователей"""
    recipe_list = Recipe.objects.all()
    recipes_by_tags = get_recipes_by_tags(request, recipe_list)
    paginator = Paginator(recipes_by_tags.get('recipes'), ITEMS)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, **recipes_by_tags}
    return render(request, 'index.html', context)


def profile(request, username):
    """Показывает страницу автора рецепта"""
    user = request.user
    author = get_object_or_404(User, username=username)
    recipe_list = author.recipes.order_by('-pub_date')
    recipes_by_tags = get_recipes_by_tags(request, recipe_list)
    paginator = Paginator(recipes_by_tags.get('recipes'), ITEMS)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'user': user,
        'author': author,
        'page': page,
        'paginator': paginator,
        **recipes_by_tags
    }
    return render(request, 'authorRecipe.html', context)


def recipe_view(request, recipe_id):
    """Показывает страницу рецепта"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, username=recipe.author)
    user = request.user
    context = {'recipe': recipe, 'author': author, 'user': user}
    return render(request, 'singlePage.html', context)


@login_required
def new_recipe(request):
    """Создаёт новый рецепт"""
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request.POST)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')

        if form.is_valid():
            recipe_form_save(form, ingredients, request)
            return redirect('index')

    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def recipe_edit(request, recipe_id):
    """Изменяет рецепт"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ing = Amount.objects.filter(recipe=recipe_id)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
    context = {'form': form, 'recipe': recipe, 'ingredients': ing}

    if recipe.author == request.user:
        if request.method == 'POST':
            ingredients = get_ingredients(request.POST)

            if form.is_valid():
                ing.delete()
                recipe_form_save(form, ingredients, request)
                return redirect('recipe_view', recipe_id)

        return render(request, 'formChangeRecipe.html', context)
    else:
        return redirect('recipe_view', recipe_id)


@login_required
def recipe_delete(request, recipe_id):
    """Удаляет рецепт"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author == request.user:
        if request.method == 'GET':
            recipe.delete()
            return render(request, 'recipe_delete.html')
    return redirect('recipe_view', recipe_id)


@login_required
def subscribe(request):
    """Предоставляет список подписок пользователя"""
    user = request.user
    subscriptions = Subscribe.objects.filter(user=user)
    paginator = Paginator(subscriptions, ITEMS)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'subscriptions': subscriptions,
        'user': user
    }
    return render(request, 'myFollow.html', context)


@login_required
def favorite(request):
    """Предоставляет список любимых рецептов пользователя"""
    user = request.user
    favorites_list = Recipe.objects.favorites(user=user)
    favorites_by_tags = get_recipes_by_tags(request, favorites_list)
    paginator = Paginator(favorites_by_tags.get('recipes'), ITEMS)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, **favorites_by_tags}
    return render(request, 'favorite.html', context)


@login_required
def purchase(request):
    """Показывает рецепты, добавленные в список покупок"""
    user = request.user
    purchases = Recipe.objects.purchases(user=user)
    context = {'recipes': purchases}
    return render(request, 'shopList.html', context)


@login_required
def remove_from_purchases(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    Purchase.objects.filter(recipe=recipe, user=request.user).delete()
    return redirect('purchases')


def download_list(request):
    sh_list = shopping_list(request)
    ingredient_txt = []
    for product, quantity in sh_list.items():
        for key, value in quantity.items():
            ingredient_txt += [f'{product.capitalize()} ({key}) - {value} \n']
    filename = 'ingredients.txt'
    response = HttpResponse(ingredient_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
