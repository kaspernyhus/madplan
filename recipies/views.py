from django.shortcuts import render
from .models import *


def show_recipies(request):
    all_recipies = Recipies.objects.all()
    
    recipies = []
    for recipe in all_recipies:
        recipies.append({'name': recipe.name, 'type': recipe.get_type(), 'id':recipe.id})
    
    context = {'recipies': recipies}
    return render(request, 'recipies/index.html', context)


def show_recipe(request, recipe_id):
    # Get recipe data
    recipe_data = Recipies.objects.all().filter(pk=recipe_id)
    for data in recipe_data:
        recipe = {'id': data.id, 'name': data.name, 'date': data.date, 'description': data.description}

    # Get recipe ingredients
    recipe_ingredients = RecipeIngredients.objects.all().filter(recipe_id=recipe_id)
    ingredients = []
    for ingredient in recipe_ingredients:
        ingredients.append({'name': ingredient.get_ingredient_name(), 'unit': ingredient.get_unit_name(), 'amount': ingredient.amount})

    context = {'recipe': recipe, 'ingredients': ingredients}
    return render(request, 'recipies/recipe.html', context)


def edit_recipe(request, recipe_id):
    # Get recipe data
    recipe_data = Recipies.objects.all().filter(pk=recipe_id)
    for data in recipe_data:
        recipe = {'id': data.id, 'name': data.name, 'date': data.date, 'description': data.description}

    # Get the infredients in the recipe
    recipe_ingredients_quary = RecipeIngredients.objects.all().filter(recipe_id=recipe_id)

    recipe_ingredients = []
    for ingredient in recipe_ingredients_quary:
        recipe_ingredients.append({'name': ingredient.get_ingredient_name(), 'unit': ingredient.get_unit_name(), 'amount': ingredient.amount})
    
    # Get a list of all avaiable ingredients
    all_ingredients_quary = Ingredients.objects.all()
    all_ingredients = []
    for ingredient in all_ingredients_quary:
        all_ingredients.append({'name': ingredient.name, 'description': ingredient.description})

    context = {'recipe': recipe, 'recipe_ingredients': recipe_ingredients, 'all_ingredients': all_ingredients}

    return render(request, 'recipies/edit_recipe.html', context)

