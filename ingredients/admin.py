from django.contrib import admin
from .models import *





class IngredientsAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'description', 'category', 'best_before', 'price')

  

admin.site.register(Ingredients, IngredientsAdmin)
