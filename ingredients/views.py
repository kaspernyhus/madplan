from django.shortcuts import render, redirect
from .models import *
from .forms import NewIngredientForm

def show_ingredients_list(request):
    all_ingredients = Ingredients.objects.all()

    ingredients = []
    for ingredient in all_ingredients:
        ingredients.append({'name': ingredient.name, 'description': ingredient.description})

    context = {'ingredients': ingredients}
    return render(request, 'ingredients/ingredients.html', context)


def new_ingredient(request):
    # if request.method == 'GET':
    #     print(request.GET)
    if request.method == 'POST':
        form = NewIngredientForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('/')

    form = NewIngredientForm()

    return render(request, 'ingredients/new_ingredient.html', {'form': form} )