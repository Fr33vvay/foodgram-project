from django.urls import path

from . import views

urlpatterns = [
    path('recipe/new/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete/', views.recipe_delete,
         name='recipe_delete'),
    path('recipe/<tag>/', views.index_tag, name='tag_index'),
    path('subscriptions/', views.subscribe, name='subscribe'),
    path('<username>/', views.profile, name='profile'),

    path('', views.index, name='index'),
]
