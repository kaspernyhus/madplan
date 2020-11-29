from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.view_foodplans, name='view_foodplans'),
  path('new/', views.create_foodplan, name='create_foodplan'),
  ]