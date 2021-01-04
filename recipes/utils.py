from recipes.models import Tag


def get_ingredients(data):
    """Создает список выбранных при создании рецепта ингредиентов"""
    ingredient_numbers = set()
    ingredients = []
    for key in data:
        if key.startswith('nameIngredient_'):
            _, number = key.split('_')
            ingredient_numbers.add(number)
    for number in ingredient_numbers:
        ingredients.append(
            {
                'title': data[f'nameIngredient_{number}'],
                'dimension': data[f'unitsIngredient_{number}'],
                'quantity': float(data[f'valueIngredient_{number}']),
            }
        )
    return ingredients


def get_recipes_by_tags(request, recipes):
    """Возвращает набор рецептов в зависимости от выбранных тегов"""
    filters = ''
    tags = Tag.objects.all()
    current_tags = request.GET.getlist('filters')
    for tag in current_tags:
        filters += '&filters=' + tag
    if current_tags:
        recipes = recipes.filter(tag__title__in=current_tags).distinct()
    context = {'recipes': recipes, 'tags': tags, 'filters': filters}
    return context
