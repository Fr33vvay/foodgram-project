from django.urls import include, path

from api.views import (IngredientListView, SubscribeViewSet,
                       FavoriteRecipeViewSet)
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientListView)
router_v1.register('subscriptions', SubscribeViewSet)
router_v1.register('favorites', FavoriteRecipeViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
