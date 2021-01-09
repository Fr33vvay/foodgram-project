from recipes.models import Tag, Amount, Ingredient


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


def shopping_list(request):
    shopper = request.user
    shop_list = shopper.purchases.all()
    ingredients = {}
    for item in shop_list:
        for obj in item.recipe.recipe_amount.all():
            title = obj.ingredient.title
            dimension = obj.ingredient.dimension
            if title in ingredients:
                ingredients[title][dimension] += obj.quantity
            else:
                ingredients[title] = {dimension: 0}
                ingredients[title][dimension] += obj.quantity
    return ingredients


def recipe_form_save(form, ingredients, request):
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
