from django.urls import path, include
from . import views

urlpatterns = [
    path('ingredients_list', views.show_ingredients_list, name='show_ingredients_list'),
    path('new_ingredient', views.new_ingredient, name='new_ingredient'),
  ]