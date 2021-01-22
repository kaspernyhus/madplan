from django.contrib import admin
from .models import *

admin.site.register(RecipeTypes)
admin.site.register(RecipeTags)
admin.site.register(Recipies)
admin.site.register(MeasurementUnits)
admin.site.register(RecipeIngredients)
admin.site.register(RecipeIngredientsHeading)
admin.site.register(RecipeInstructions)