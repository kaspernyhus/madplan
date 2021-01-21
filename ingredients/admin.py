from django.contrib import admin
from .models import *


class IngredientsAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'description', 'category', 'best_before', 'price')


class IngredientCategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'shop_order')

  
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(IngredientCategory, IngredientCategoryAdmin)
