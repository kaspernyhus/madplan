from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_recipies, name='show_recipies'),
    path('<int:recipe_id>/', views.show_recipe, name='show_recipe'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
  ]
