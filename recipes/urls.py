from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/new/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete/', views.recipe_delete,
         name='recipe_delete'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/sub', views.subscribe, name='subscribe')
]
