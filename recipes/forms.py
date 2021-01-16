from django.forms import ModelForm, forms

from recipes.models import Recipe, Ingredient


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'name',
            'tag',
            'cooking_time',
            'description',
            'image',
        )

    # def clean_ingredient(self):
    #     """Валидатор для ингридиентов"""
    #     ingredient_names = self.data.getlist('nameIngredient')
    #     ingredient_dimension = self.data.getlist('unitsIngredient')
    #     ingredient_quantity = self.data.getlist('valueIngredient')
    #     ingredients_clean = []
    #     for ingredient in zip(ingredient_names, ingredient_dimension,
    #                           ingredient_quantity):
    #         if Ingredient.objects.filter(title=ingredient[0]).exists():
    #             ingredients_clean.append({'title': ingredient[0],
    #                                       'dimension': ingredient[1],
    #                                       'quantity': ingredient[2]})
    #     if len(ingredients_clean) == 0:
    #         raise forms.ValidationError('Добавте ингридиент')
    #     return ingredients_clean
