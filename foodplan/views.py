from django.shortcuts import render, redirect
from .models import *
from recipies.models import Recipies
from django.views.generic import DeleteView


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
    return render(request, 'pages/foodplans.html', context)


def view_foodplan(request, foodplan_id):
    # delete recipe in current foodplan
    if request.method == 'POST':
        recipe_id = request.POST.get('name')
        foodplan = Foodplans.objects.get(foodplan_id=foodplan_id, recipe_id=recipe_id)
        foodplan.delete()
    
    # Get the recipies currently in active foodplan
    foodplan = Foodplans.objects.all().filter(foodplan_id=foodplan_id)
    recipies = []
    for recipe in foodplan:
        recipies.append({'name': recipe.get_recipe_name(), 'id': recipe.recipe_id})
    
    if not recipies: # if there is no more recipies in current foodplan
        return redirect('/foodplans/')

    context = {'recipies': recipies, 'created_date': foodplan[0].date, 'foodplan_id': foodplan_id }
    return render(request, 'pages/foodplan.html', context)


def create_foodplan(request):
    # Get next available foodplan ID
    latest = Foodplans.objects.latest('foodplan_id')
    next_id = latest.foodplan_id + 1
    return redirect('/foodplans/edit/' + str(next_id))


def edit_foodplan(request, foodplan_id):
    # add or delete foodplan from active foodplan
    if request.method == 'POST':
        recipe_id = request.POST.get('delete')
        if recipe_id is not None:
            foodplan = Foodplans.objects.get(foodplan_id=foodplan_id, recipe_id=recipe_id)
            foodplan.delete()
        recipe_id = request.POST.get('add')
        if recipe_id is not None:
            foodplan = Foodplans(foodplan_id=foodplan_id, recipe_id=recipe_id)
            foodplan.save()
        
    # Get the recipies currently in active foodplan
    foodplans = Foodplans.objects.all().filter(foodplan_id=foodplan_id)
    foodplan_recipe_ids = [0]
    for foodplan in foodplans:
        foodplan_recipe_ids.append(foodplan.recipe_id)

    # Make a list of all recipies
    all_recipies = Recipies.objects.all()
    recipies = []
    for recipe in all_recipies:
        recipies.append({'name': recipe.name, 'type': recipe.get_type(), 'id': recipe.id})

    context = {'recipies': recipies, 'foodplan_id': foodplan_id, 'foodplan_recipe_ids':foodplan_recipe_ids}
    return render(request, 'pages/edit_foodplan.html', context)


# def add_foodplan_recipe(request, foodplan_id, recipe_id):
#     foodplan = Foodplans(foodplan_id=foodplan_id, recipe_id=recipe_id)
#     foodplan.save()
#     return redirect('/foodplans/edit/' + str(foodplan_id))


# def delete_foodplan_recipe(request, foodplan_id, recipe_id):
#     try:
#         foodplan = Foodplans.objects.get(foodplan_id=foodplan_id, recipe_id=recipe_id)
#         foodplan.delete()
#     except:
#         pass
#     print('---------------------')
#     print(request)
#     print(request.META.get('HTTP_REFERER'))
#     print('---------------------')
#     return redirect('/foodplans/edit/' + str(foodplan_id))
    

    
def delete_foodplan(request, foodplan_id):
    foodplans = Foodplans.objects.all().filter(foodplan_id=foodplan_id)
    for foodplan in foodplans:
        foodplan.delete()
    return redirect('/foodplans/')