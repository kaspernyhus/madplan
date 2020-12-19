from django.shortcuts import render, redirect
from .models import *
from recipies.models import Recipies
from recipies.forms import RecipeTypeFilterBox
from django.views.generic import DeleteView
from random import shuffle


def view_foodplans(request):
    all_foodplans = Foodplans.objects.all().order_by('-date')
    # select most recent foodplan entry per foodplan (remove duplicates)
    foodplans = []
    seen_ids = []
    for foodplan in all_foodplans:
        if foodplan.foodplan_id not in seen_ids:
            seen_ids.append(foodplan.foodplan_id)
            foodplans.append(foodplan)
    
    context = {'foodplans': foodplans}
    return render(request, 'foodplans/foodplans.html', context)


def view_foodplan(request, foodplan_id):
    # delete recipe in current foodplan
    if request.method == 'POST':
        if request.POST.getlist('delete_recipe'):
            recipe_id = request.POST.getlist('delete_recipe')
            foodplan = Foodplans.objects.get(foodplan_id=foodplan_id, recipe_id=recipe_id[0])
            foodplan.delete()
        elif request.POST.getlist('edit_quantity'):
            recipe_ids = request.POST.getlist('recipe_id')
            quantities = request.POST.getlist('qty')
            print('Recipe ids:', recipe_ids)
            print('Qty: ', quantities)
            for i, recipe_id in enumerate(recipe_ids):
                foodplan = Foodplans.objects.get(foodplan_id=foodplan_id, recipe_id=recipe_id)
                foodplan.quantity = quantities[i]
                foodplan.save()
    # Get the recipies currently in active foodplan
    foodplan = Foodplans.objects.all().filter(foodplan_id=foodplan_id)
    recipies = []
    for recipe in foodplan:
        recipies.append({'name': recipe.get_recipe_name(), 'id': recipe.recipe_id, 'quantity': recipe.quantity})
    if not recipies: # if there is no more recipies in current foodplan
        return redirect('/foodplans/')

    # Foodplan status
    status = FoodplanStatus.objects.get(foodplan_id=foodplan_id)

    context = {'recipies': recipies, 'created_date': foodplan[0].date, 'foodplan_id': foodplan_id, 'status': status }
    return render(request, 'foodplans/foodplan.html', context)


def create_foodplan(request):
    # Get next available foodplan ID
    try:
        latest = Foodplans.objects.latest('foodplan_id')
        next_id = latest.foodplan_id + 1
    except:
        next_id = 1
    # Create FoodplanStatus entry
    foodplan_status = FoodplanStatus(pk=next_id)
    foodplan_status.save()
    return redirect('/foodplans/edit/' + str(next_id))


def edit_foodplan(request, foodplan_id):
    # Get recipies based on filter boxes
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
    else: # Get all recipies in db
        form = RecipeTypeFilterBox()
        recipies_query = Recipies.objects.all()
    # add or delete foodplan from active foodplan
    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            recipe_id = request.POST.get('delete')
            foodplan = Foodplans.objects.get(foodplan_id=foodplan_id, recipe_id=recipe_id)
            foodplan.delete()
        else:
            recipe_id = request.POST.get('add')
            quantity = request.POST.get('quantity')
            foodplan = Foodplans(foodplan_id=foodplan_id, recipe_id=recipe_id, quantity=quantity)
            foodplan.save()   
    # Get the foodplan recipies and their quantity currently in active foodplan
    foodplan_quaryset = Foodplans.objects.all().filter(foodplan_id=foodplan_id)
    foodplan = []
    foodplan_recipies = [0]
    for recipe in foodplan_quaryset:
        foodplan.append({'recipe_id': recipe.recipe_id, 'quantity': recipe.quantity})
        foodplan_recipies.append(recipe.recipe_id)

    # Randomize recipies order
    #shuffle(recipies_query)

    context = {'all_recipies': recipies_query, 'foodplan_recipies':foodplan_recipies, 'foodplan_id': foodplan_id, 'form': form}
    return render(request, 'foodplans/edit_foodplan.html', context)

    
def delete_foodplan(request, foodplan_id):
    foodplans = Foodplans.objects.all().filter(foodplan_id=foodplan_id)
    for foodplan in foodplans:
        foodplan.delete()
    return redirect('/foodplans/')



