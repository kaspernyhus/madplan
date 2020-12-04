from django.shortcuts import render
from .models import *

def show_ingredients_list(request):
    all_ingredients = Ingredients.objects.all()

    ingredients = []
    for ingredient in all_ingredients:
        ingredients.append({'name': ingredient.name, 'description': ingredient.description})

    context = {'ingredients': ingredients}
    return render(request, 'recipies/ingredients.html', context)


def new_ingredient(request):
    

    return render(request, 'recipies/new_ingredient.html')
