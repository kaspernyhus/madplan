from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_recipies, name='show_recipies'),
    path('<int:recipe_id>/', views.show_recipe, name='show_recipe'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('edit/name/<int:recipe_id>/', views.edit_recipe_name, name='edit_recipe_name'),
    path('edit/recipe_ingredient/<int:recipe_ingredient_id>/', views.edit_reciep_ingredient, name='edit_recipe_ingredient'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
  ]
