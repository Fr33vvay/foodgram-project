from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class RecipeManager(models.Manager):
    def favorites(self, user):
        favorite_recipes_ids = list(FavoriteRecipe.objects.filter(
            user=user).values_list('recipe_id', flat=True))
        return self.get_queryset().filter(id__in=favorite_recipes_ids)


class Ingredient(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    dimension = models.CharField(verbose_name='Единицы измерения',
                                 max_length=50)

    def __str__(self):
        return f'{self.title} ({self.dimension})'

    class Meta:
        ordering = ['title']
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Tag(models.Model):
    title = models.CharField(verbose_name='Имя тега', max_length=150)
    color = models.CharField(verbose_name='Цвет', max_length=15, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Recipe(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    author = models.ForeignKey(User, verbose_name='Автор',
                               related_name='recipes',
                               on_delete=models.CASCADE)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True,
                                    db_index=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Картинка', upload_to='recipes/',
                              blank=True, null=True)
    ingredient = models.ManyToManyField(Ingredient, through='Amount',
                                        related_name='amount')
    tag = models.ManyToManyField(Tag, related_name='recipe_tag')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки')

    objects = RecipeManager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class Amount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_amount')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredient_amount')
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'Из рецепта "{self.recipe}"'

    class Meta:
        verbose_name = "Количество"
        verbose_name_plural = "Количество"


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites')

    class Meta:
        ordering = ['-id']
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
