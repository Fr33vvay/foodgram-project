from django.shortcuts import get_object_or_404

from api.serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    PurchaseSerializer,
    SubscribeSerializer
)
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Purchase,
    Recipe,
    Subscribe,
    User
)
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
        serializer = SubscribeSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, author=author)
        return Response({'success': True})

    def destroy(self, request, *args, **kwargs):
        """Удаляет подписку на автора"""
        Subscribe.objects.filter(author__id=kwargs['pk'],
                                 user=request.user).delete()
        return Response({'success': True})


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Добавляет рецепт в 'Избранное'"""
        recipe = get_object_or_404(Recipe, pk=self.request.data.get('id'))
        serializer = FavoriteRecipeSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, recipe=recipe)
        return Response({'success': True})

    def destroy(self, request, *args, **kwargs):
        """Удаляет рецепт из 'Избранного'"""
        FavoriteRecipe.objects.filter(recipe__id=kwargs['pk'],
                                      user=request.user).delete()
        return Response({'success': True})


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Добавляет рецепт в список покупок"""
        recipe = get_object_or_404(Recipe, pk=self.request.data.get('id'))
        serializer = PurchaseSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, recipe=recipe)
        return Response({'success': True})

    def destroy(self, request, *args, **kwargs):
        """Удаляет рецепт из списка покупок"""
        Purchase.objects.filter(recipe__id=kwargs['pk'],
                                user=request.user).delete()
        return Response({'success': True})
