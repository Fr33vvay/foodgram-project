from django.shortcuts import get_object_or_404

from api.models import Subscribe
from api.serializers import IngredientSerializer, SubscribeSerializer
from recipes.models import Ingredient, User
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
        serializer = SubscribeSerializer(data=self.request.data, context={
            'request_user': self.request.user,
            'author': author
        })
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, author=author)
        return Response({'success': True})

    def destroy(self, request, *args, **kwargs):
        """Удаляет подписку на автора"""
        author = get_object_or_404(User, pk=kwargs['pk'])
        follow = get_object_or_404(Subscribe, author=author, user=request.user)
        follow.delete()
        return Response({'success': True})
