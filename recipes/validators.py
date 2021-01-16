from django.core.exceptions import ValidationError


def validate_file(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError('Максимальный размер файла - 2 Мб')


# def validate_ingredient(self):
#         """Валидатор для ингридиентов"""
#         ingredient_names = self.data.getlist('nameIngredient')
#         ingredient_dimension = self.data.getlist('unitsIngredient')
#         ingredient_quantity = self.data.getlist('valueIngredient')
#         ingredients_clean = []
#         for ingredient in zip(ingredient_names, ingredient_dimension,
#                               ingredient_quantity):
#             if Ingredient.objects.filter(title=ingredient[0]).exists():
#                 ingredients_clean.append({'title': ingredient[0],
#                                           'dimension': ingredient[1],
#                                           'quantity': ingredient[2]})
#         if len(ingredients_clean) == 0:
#             raise forms.ValidationError('Добавте ингридиент')
#         return ingredients_clean