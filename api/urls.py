from django.urls import include, path

from api.views import (
    FavoriteRecipeViewSet,
    IngredientListView,
    SubscribeViewSet,
    PurchaseViewSet
)
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientListView)
router_v1.register('subscriptions', SubscribeViewSet)
router_v1.register('favorites', FavoriteRecipeViewSet)
router_v1.register('purchases', PurchaseViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
