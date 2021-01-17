from django.core.exceptions import ValidationError
from django.forms import ModelForm

from recipes.models import Ingredient, Recipe


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

    def clean(self):
        known_ids = []
        for items in self.data.keys():
            if 'nameIngredient' in items:
                name, id = items.split('_')
                known_ids.append(id)

        for id in known_ids:
            title = self.data.get(f'nameIngredient_{id}')
            value = self.data.get(f'valueIngredient_{id}')

            if int(value) <= 0:
                raise ValidationError('Ингредиентов должно быть больше 0')

            is_exists = Ingredient.objects.filter(title=title).exists()

            if not is_exists:
                raise ValidationError(
                    'Выберите ингредиент из выпадающего списка')
