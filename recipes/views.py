from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Recipe, User


def index(request):
    """Предоставляет список рецептов для всех пользователей"""
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    template_name = (
        'indexAuth.html' if request.user.is_authenticated
        else 'indexNotAuth.html')
    return render(request, template_name, {'page': page,
                                           'paginator': paginator})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipe_list = author.recipes.order_by('-pub_date')
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'authorRecipe.html', {'author': author,
                                                 'page': page,
                                                 'paginator': paginator})


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(author.recipes, id=recipe_id)
    template_name = (
        'singlePage.html' if request.user.is_authenticated
        else 'singlePageNotAuth.html')
    return render(request, template_name, {'author': author,
                                           'recipe': recipe})
