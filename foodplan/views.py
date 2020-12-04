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
        if request.POST.get('delete') is not None:
            recipe_id = request.POST.get('delete')
            foodplan = Foodplans.objects.get(foodplan_id=foodplan_id, recipe_id=recipe_id)
            foodplan.delete()
        else:
            recipe_id = request.POST.get('edit_quantity')
            new_quantity = request.POST.get('quantity')
            foodplan = Foodplans.objects.get(foodplan_id=foodplan_id, recipe_id=recipe_id)
            foodplan.quantity = new_quantity
            foodplan.save()

    
    # Get the recipies currently in active foodplan
    foodplan = Foodplans.objects.all().filter(foodplan_id=foodplan_id)
    recipies = []
    for recipe in foodplan:
        recipies.append({'name': recipe.get_recipe_name(), 'id': recipe.recipe_id, 'quantity': recipe.quantity})
    
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
        if request.POST.get('delete') is not None:
            recipe_id = request.POST.get('delete')
            foodplan = Foodplans.objects.get(foodplan_id=foodplan_id, recipe_id=recipe_id)
            foodplan.delete()
        else:
            recipe_id = request.POST.get('add')
            quantity = request.POST.get('quantity')
            foodplan = Foodplans(foodplan_id=foodplan_id, recipe_id=recipe_id, quantity=quantity)
            foodplan.save()
            
        
    # Get the recipies and their quantity currently in active foodplan
    foodplan_quaryset = Foodplans.objects.all().filter(foodplan_id=foodplan_id)
    
    foodplan = []
    foodplan_recipies = [0]

    for recipe in foodplan_quaryset:
        foodplan.append({'recipe_id': recipe.recipe_id, 'quantity': recipe.quantity})
        foodplan_recipies.append(recipe.recipe_id)


    # Make a list of all recipies
    recipies_quaryset = Recipies.objects.all()
    all_recipies = []
    for recipe in recipies_quaryset:
        all_recipies.append({'name': recipe.name, 'type': recipe.get_type(), 'id': recipe.id})

    context = {'all_recipies': all_recipies, 'foodplan_recipies':foodplan_recipies, 'foodplan_id': foodplan_id, }
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