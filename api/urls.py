from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientListView


router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientListView)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

