from django.forms import ModelForm
from django import forms
from recipes.models import Recipe


class RecipeForm(ModelForm):
    image = forms.ImageField(required=True, label='Картинка')

    class Meta:
        model = Recipe
        fields = (
            'name',
            'tag',
            'cooking_time',
            'description',
            'image',
        )
