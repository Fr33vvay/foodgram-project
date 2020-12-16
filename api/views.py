from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, permissions
from rest_framework.response import Response

from api.serializers import IngredientSerializer, SubscribeSerializer
from recipes.models import Ingredient, Subscribe, User


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
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Удаляет подписку на автора"""
        author = get_object_or_404(User, pk=kwargs['pk'])
        follow = get_object_or_404(Subscribe, author=author, user=request.user)
        follow.delete()
        return Response({'success': True})
