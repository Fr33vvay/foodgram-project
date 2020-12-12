from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect

from recipes.models import Recipe, User, Ingredient, Amount
from recipes.forms import RecipeForm
from recipes.utils import get_ingredients


def index(request):
    """Предоставляет список рецептов для всех пользователей"""
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    template_name = ('indexAuth.html')
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
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, username=recipe.author)
    context = {'recipe': recipe, 'author': author}
    template_name = (
        'singlePage.html' if request.user.is_authenticated
        else 'singlePageNotAuth.html')
    return render(request, template_name, context)


@login_required
def new_recipe(request):
    user = get_object_or_404(User, username=request.user)
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if request.method == 'POST':
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for ing_name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=ing_name)
                recipe_ing = Amount(recipe=recipe,
                                    ingredient=ingredient,
                                    quantity=quantity)
                recipe_ing.save()
            form.save_m2m()
            return redirect('index')
        else:
            render(request, 'formRecipe.html', {'form': form})
    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})
