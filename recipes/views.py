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


    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request.POST)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')

        if form.is_valid():
            print('valid')
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
        else:
            print('not valid')
    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})
