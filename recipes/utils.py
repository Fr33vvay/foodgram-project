# def get_ingredients(request):
#     ingredients = {}
#     for key, ingredient_name in request.POST.items():
#         if 'nameIngredient' in key:
#             _ = key.split('_')
#             ingredients[ingredient_name] = int(request.POST[
#                                                    f'valueIngredient_{_[1]}'])
#     return ingredients

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
                'quantity': int(data[f'valueIngredient_{number}']),
            }
        )
    return ingredients