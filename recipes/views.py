from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Recipe


def recipes(request):
    '''Предоставляет список рецептов для всех пользователей'''
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    template_name = (
        'indexAuth.html'
        if request.user.is_authenticated
        else 'indexNotAuth.html'
    )
    return render(request, template_name, {
            'page': page,
            'paginator': paginator,
        },
    )
