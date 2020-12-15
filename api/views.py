from rest_framework import filters, mixins, viewsets

from api.serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Возвращает json ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title', ]
