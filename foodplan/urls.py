from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.view_foodplans, name='view_foodplans'),
  path('<int:foodplan_id>/', views.view_foodplan, name='view_foodplan'),
  path('new_foodplan/', views.create_foodplan, name='create_foodplan'),
  path('edit/<int:foodplan_id>/', views.edit_foodplan, name='edit_foodplan'),
  # path('add/<int:foodplan_id>/<int:recipe_id>', views.add_foodplan_recipe, name='add_foodplan_recipe'),
  # path('delete/<int:foodplan_id>/<int:recipe_id>', views.delete_foodplan_recipe, name='delete_foodplan_recipe'),
  path('delete_foodplan/<int:foodplan_id>/', views.delete_foodplan, name='delete_foodplan'),
  ]