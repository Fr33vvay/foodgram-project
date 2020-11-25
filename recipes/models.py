from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Unit(models.Model):
    name = models.CharField(verbose_name='Название', max_length=20,
                            unique=True)


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200,
                            unique=True)
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')
    unit = models.ForeignKey(Unit, verbose_name='Единицы измерения',
                             on_delete=models.SET_NULL)


class Tag(models.TextChoices):
    """
    Теги для модели Recipe
    """
    BREAKFAST = 'breakfast', 'Завтрак'
    LUNCH = 'lunch', 'Обед'
    DINNER = 'dinner', 'Ужин'


class Recipe(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200,
                            unique=True)
    author = models.ForeignKey(User, verbose_name='Автор',
                               related_name='recipes',
                               on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    ingredient = models.ManyToManyField(Ingredient, verbose_name='Ингредиенты',
                                        related_name='ingredients')
    tag = models.CharField(choices=Tag.choices, default=Tag.BREAKFAST,
                           max_length=50, verbose_name='Тег')
    cooktime = models.PositiveSmallIntegerField(verbose_name='Время готовки')
    slug = models.SlugField(max_length=100, unique=True)


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Подписчик',
                             related_name='subscribers')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='subscriptions')
