from django.urls import path

from . import views

urlpatterns = [
    path('recipe/', views.index, name='index'),
    path('recipe/new/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete/', views.recipe_delete,
         name='recipe_delete'),
    path('recipe/favorites/', views.favorite, name='favorites'),
    path('recipe/purchases/', views.purchase, name='purchases'),
    path('recipe/purchase_delete/<int:recipe_id>/',
         views.remove_from_purchases, name='delete_purchase'),
    path('shoplist/', views.download_list, name='download'),
    path('subscriptions/', views.subscribe, name='subscribe'),
    path('<username>/', views.profile, name='profile'),
]
