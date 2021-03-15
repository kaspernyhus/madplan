from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index_foodplans, name='index_foodplans'),
  path('<int:foodplan_id>/', views.view_foodplan, name='view_foodplan'),
  path('new_foodplan/', views.create_foodplan, name='create_foodplan'),
  path('edit/<int:foodplan_id>/', views.edit_foodplan, name='edit_foodplan'),
  path('delete_foodplan/<int:foodplan_id>/', views.delete_foodplan, name='delete_foodplan'),
  ]