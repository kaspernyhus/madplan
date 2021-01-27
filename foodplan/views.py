from django.shortcuts import render, redirect
from .models import *
from todo.models import Shoppinglist, Task
from recipies.models import Recipies
from recipies.forms import RecipeTypeFilterBox
from django.views.generic import DeleteView
from random import shuffle


def view_foodplans(request):
    foodplans = Foodplans.objects.all().order_by('-date')
    
    context = {'foodplans': foodplans}
    return render(request, 'foodplans/foodplans.html', context)


def view_foodplan(request, foodplan_id):
    # delete recipe in current foodplan
    if request.method == 'POST':
        if request.POST.getlist('delete_recipe'):
            recipe_id = request.POST.getlist('delete_recipe')
            foodplan = Foodplans.objects.get(pk=foodplan_id)
            foodplan.delete()
        elif request.POST.getlist('edit_quantity'):
            foodplanrecipies_ids = request.POST.getlist('foodplanrecipies_id')
            quantities = request.POST.getlist('qty')
            for i, foodplanrecipies_id in enumerate(foodplanrecipies_ids):
                foodplan = FoodplanRecipies.objects.get(pk=foodplanrecipies_id)
                foodplan.quantity = quantities[i]
                foodplan.save()

    # Get the recipies currently in active foodplan
    foodplan = FoodplanRecipies.objects.all().filter(foodplan_id=foodplan_id)
    recipies = []
    for recipe in foodplan:
        recipe_obj = Recipies.objects.get(pk=recipe.recipe_id)
        recipies.append({'recipe_obj': recipe_obj, 'foodplan_obj': recipe})
    if not recipies: # if there is no more recipies in current foodplan
        return redirect('/foodplans/')
    # Foodplan entry
    foodplan_quary = Foodplans.objects.get(pk=foodplan_id)
    # Shoppinglist id
    try:
        shoppinglist_id_quary = Shoppinglist.objects.all().filter(list_source='foodplan', source_id=foodplan_id)
        shoppinglist_id = shoppinglist_id_quary[0].id
    except:
        shoppinglist_id = 1

    context = {'recipies': recipies, 'created_date': foodplan_quary.date, 'foodplan_id': foodplan_id, 'complete': foodplan_quary.complete, 'shoppinglist_id': shoppinglist_id }
    return render(request, 'foodplans/foodplan.html', context)


def create_foodplan(request):
    foodplan = Foodplans()
    foodplan.save()

    return redirect('/foodplans/edit/' + str(foodplan.id))


def edit_foodplan(request, foodplan_id):
    # Get all recipies in db
    form = RecipeTypeFilterBox()
    recipies_query = Recipies.objects.all() #.order_by('?') # shuffle/random order
    
    # Get recipies based on filter boxes
    if request.method == 'GET':
        if request.GET.get('recipe_type') and request.GET.get('tags'):
            filter_by_type = request.GET.get('recipe_type')
            filter_by_tags = request.GET.get('tags')
            recipies_query = Recipies.objects.filter(recipe_type_id=filter_by_type, tags=filter_by_tags)
            form = RecipeTypeFilterBox(initial={'recipe_type': filter_by_type, 'tags': filter_by_tags})
        elif request.GET.get('recipe_type'):
            filter_by = request.GET.get('recipe_type')
            recipies_query = Recipies.objects.filter(recipe_type_id=filter_by)
            form = RecipeTypeFilterBox(initial={'recipe_type': filter_by})
        elif request.GET.get('tags'):
            filter_by = request.GET.get('tags')
            recipies_query = Recipies.objects.filter(tags=filter_by)
            form = RecipeTypeFilterBox(initial={'tags': filter_by})
        # add or delete foodplan from active foodplan
    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            recipe_id = request.POST.get('delete')
            foodplan = Foodplans.objects.get(foodplan_id=foodplan_id, recipe_id=recipe_id)
            foodplan.delete()
        else:
            recipe_id = request.POST.get('add')
            quantity = request.POST.get('quantity')
            foodplan_recipe = FoodplanRecipies(foodplan_id=foodplan_id, recipe_id=recipe_id, quantity=quantity)
            foodplan_recipe.save()   
    # Get the foodplan recipies and their quantity currently in active foodplan
    foodplan_quaryset = FoodplanRecipies.objects.all().filter(foodplan_id=foodplan_id)
    foodplan = []
    foodplan_recipies = [0]
    for recipe in foodplan_quaryset:
        foodplan.append({'recipe_id': recipe.recipe_id, 'quantity': recipe.quantity})
        foodplan_recipies.append(recipe.recipe_id)

    context = {'all_recipies': recipies_query, 'foodplan_recipies':foodplan_recipies, 'foodplan_id': foodplan_id, 'form': form}
    return render(request, 'foodplans/edit_foodplan.html', context)

    
def delete_foodplan(request, foodplan_id):
    try:
        shoppinglist = Shoppinglist.objects.get(list_source='foodplan', source_id=foodplan_id)
        shoppinglist.delete()
    except:
        pass
    foodplan = Foodplans.objects.get(pk=foodplan_id)
    foodplan.delete()
    
    return redirect('/foodplans/')



