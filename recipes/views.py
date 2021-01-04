from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from api.models import Subscribe
from recipes.forms import RecipeForm
from recipes.models import Amount, Ingredient, Recipe, User
from recipes.utils import get_ingredients, get_recipes_by_tags


def index(request):
    """Предоставляет список рецептов для всех пользователей"""
    recipe_list = Recipe.objects.all()
    recipes_by_tags = get_recipes_by_tags(request, recipe_list)
    paginator = Paginator(recipes_by_tags.get('recipes'), 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, **recipes_by_tags}
    return render(request, 'index.html', context)


def profile(request, username):
    """Показывает страницу автора рецепта"""
    user = request.user
    author = get_object_or_404(User, username=username)
    subscription = False
    if user.is_authenticated:
        subscription = Subscribe.objects.filter(user=user,
                                                author=author).exists()
    recipe_list = author.recipes.order_by('-pub_date')
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'user': user,
        'author': author,
        'subscription': subscription,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'authorRecipe.html', context)


def recipe_view(request, recipe_id):
    """Показывает страницу рецепта"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, username=recipe.author)
    user = request.user
    subscription = False
    if user.is_authenticated:
        subscription = Subscribe.objects.filter(user=user,
                                                author=author).exists()
    context = {'recipe': recipe, 'author': author, 'user': user,
               'subscription': subscription}
    template_name = (
        'singlePage.html' if request.user.is_authenticated
        else 'singlePageNotAuth.html')
    return render(request, template_name, context)


@login_required
def new_recipe(request):
    """Создаёт новый рецепт"""
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request.POST)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for item in ingredients:
                recipe_ing = Amount(
                    quantity=item.get('quantity'),
                    ingredient=Ingredient.objects.get(title=item.get('title')),
                    recipe=recipe)
                recipe_ing.save()
            form.save_m2m()
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
                recipe = form.save(commit=False)
                recipe.author = request.user
                recipe.save()
                for item in ingredients:
                    recipe_ing = Amount(
                        quantity=item.get('quantity'),
                        ingredient=Ingredient.objects.get(
                            title=item.get('title')),
                        recipe=recipe)
                    recipe_ing.save()
                form.save_m2m()
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
    paginator = Paginator(subscriptions, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator,
               'subscriptions': subscriptions, 'user': user}
    return render(request, 'myFollow.html', context)


@login_required
def favorite(request):
    """Предоставляет список любимых рецептов пользователя"""
    user = request.user
    favorites_list = Recipe.objects.favorites(user=user)
    favorites_by_tags = get_recipes_by_tags(request, favorites_list)
    paginator = Paginator(favorites_by_tags.get('recipes'), 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, **favorites_by_tags}
    return render(request, 'favorite.html', context)
