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
    if request.method == 'POST':
        try:
            previous_page = request.GET['next']
        except:
            previous_page = None
        form = NewIngredientForm(request.POST)
        if form.is_valid():
            form.save()
        if previous_page:
            return redirect(previous_page)
        else:
            return redirect('/')
    try:
        ingredient_name = request.GET['ing_name']
        form = NewIngredientForm(initial={'name': ingredient_name})
    except:
        ingredient_name = None
    
    if not ingredient_name:
        form = NewIngredientForm()

    return render(request, 'ingredients/new_ingredient.html', {'form': form} )