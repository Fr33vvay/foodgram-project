from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect

from recipes.models import Recipe, User, Ingredient, Amount, Subscribe
from recipes.forms import RecipeForm
from recipes.utils import get_ingredients


def index(request):
    """Предоставляет список рецептов для всех пользователей"""
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    template_name = 'index.html'
    context = {'page': page, 'paginator': paginator}
    return render(request, template_name, context)


def profile(request, username):
    """Показывает страницу автора рецепта"""
    author = get_object_or_404(User, username=username)
    recipe_list = author.recipes.order_by('-pub_date')
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'author': author, 'page': page, 'paginator': paginator}
    return render(request, 'authorRecipe.html', context)


def recipe_view(request, recipe_id):
    """Показывает страницу рецепта"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, username=recipe.author)
    context = {'recipe': recipe, 'author': author}
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
    context = {'form': form, 'recipe': recipe, 'edit': True,
               'ingredients': ing}

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
    user = request.user
    authors = Subscribe.author.filter(user=user)
    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    template_name = 'myFollow.html'
    context = {'page': page, 'paginator': paginator, 'authors': authors}
    return render(request, template_name, context)

