from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index, name='freezerstock'),
  path('add', views.create_freezer_item, name='create_freezer_stock'),
  ]