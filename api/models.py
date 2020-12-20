from django.db import models

from recipes.models import User


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Подписчик',
                             related_name='subscribers')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='subscriptions')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
