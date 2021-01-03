from django.urls import include, path

from api.views import IngredientListView, SubscribeViewSet
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientListView)
router_v1.register('subscriptions', SubscribeViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

