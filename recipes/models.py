from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# class Unit(models.Model):
#     name = models.CharField(verbose_name='Название', max_length=20,
#                             unique=True)
#
#     def __str__(self):
#         return self.name


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    dimension = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    class Tag(models.TextChoices):
        """
        Теги для модели Recipe
        """
        BREAKFAST = 'breakfast', 'Завтрак'
        LUNCH = 'lunch', 'Обед'
        DINNER = 'dinner', 'Ужин'

    name = models.CharField(verbose_name='Название', max_length=200)
    author = models.ForeignKey(User, verbose_name='Автор',
                               related_name='recipes',
                               on_delete=models.CASCADE)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True,
                                    db_index=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    ingredients = models.ManyToManyField(
        Ingredient, through='Amount', through_fields=('recipe', 'ingredient')
    )
    tag = models.CharField(choices=Tag.choices, default=Tag.BREAKFAST,
                           max_length=50, verbose_name='Тег')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Amount(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_amount'
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f'Из рецепта "{self.recipe}"'


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Подписчик',
                             related_name='subscribers')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='subscriptions')
