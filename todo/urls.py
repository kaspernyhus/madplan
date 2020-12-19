from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='todo_index'),
    path('foodplan/<int:foodplan_id>/', views.view_shoppinglist, name='view_shoppinglist'),
    path('check/<int:task_id>/', views.check_task, name='check_task'),
    path('create_shoppinglist/<int:foodplan_id>/', views.create_shoppinglist, name='create_shoppinglist'),
  ]