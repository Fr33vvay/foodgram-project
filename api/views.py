from django.shortcuts import get_object_or_404

from users.models import Subscribe
from api.serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    SubscribeSerializer,
    PurchaseSerializer
)
from recipes.models import FavoriteRecipe, Ingredient, Recipe, User, Purchase
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.response import Response


class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Возвращает json ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title', ]


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Создаёт подписку на автора"""
        author = get_object_or_404(User, pk=self.request.data.get('id'))
        serializer = SubscribeSerializer(
            data=self.request.data,
            context={
                'request_user': self.request.user,
                'author': author
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, author=author)
        return Response({'success': True})

    def destroy(self, request, *args, **kwargs):
        """Удаляет подписку на автора"""
        author = get_object_or_404(User, pk=kwargs['pk'])
        user = request.user
        follow = get_object_or_404(Subscribe, author=author, user=user)
        follow.delete()
        return Response({'success': True})


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Добавляет рецепт в 'Избранное'"""
        recipe = get_object_or_404(Recipe, pk=self.request.data.get('id'))
        serializer = FavoriteRecipeSerializer(
            data=self.request.data,
            context={'request_user': self.request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, recipe=recipe)
        return Response({'success': True})

    def destroy(self, request, *args, **kwargs):
        """Удаляет рецепт из 'Избранного'"""
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        user = request.user
        favorite = get_object_or_404(FavoriteRecipe, recipe=recipe, user=user)
        favorite.delete()
        return Response({'success': True})


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Добавляет рецепт в список покупок"""
        recipe = get_object_or_404(Recipe, pk=self.request.data.get('id'))
        serializer = PurchaseSerializer(
            data=self.request.data,
            context={'request_user': self.request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, recipe=recipe)
        return Response({'success': True})

    def destroy(self, request, *args, **kwargs):
        """Удаляет рецепт из списка покупок"""
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        user = request.user
        purchase = get_object_or_404(Purchase, recipe=recipe, user=user)
        purchase.delete()
        return Response({'success': True})
