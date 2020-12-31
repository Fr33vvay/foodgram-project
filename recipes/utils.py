from recipes.models import Tag


def get_ingredients(data):
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
    tags = Tag.objects.all()
    current_tags = request.GET.getlist('filters')
    if current_tags:
        recipes = recipes.filter(tag__title__in=current_tags).distinct()
    context = {'recipes': recipes, 'tags': tags}
    return context
