from django.shortcuts import render, redirect
from foodplan.models import Foodplans, FoodplanStatus
from recipies.models import RecipeIngredients
from .models import Task
from .forms import TaskForm
from unit_conversion.unit_conversion import convert_amount


def index(request):
  all_foodplans = Foodplans.objects.all().order_by('-date')
  # select most recent foodplan entry per foodplan (remove duplicates)
  foodplans = []
  seen_ids = []
  for foodplan in all_foodplans:
      if foodplan.foodplan_id not in seen_ids:
          seen_ids.append(foodplan.foodplan_id)
          foodplans.append(foodplan)
  
  context = {'foodplans': foodplans}
  return render(request, 'todo/index.html', context)


def view_shoppinglist(request, foodplan_id):
  tasks = Task.objects.filter(foodplan=foodplan_id).order_by('ingredient_category__shop_order')
  form = TaskForm()
  context = {'tasks': tasks, 'form': form}
  return render(request, 'todo/shoppinglist.html', context)


# Toggle task complete/incomplete
def check_task(request, task_id):
  task = Task.objects.get(pk=task_id)
  if task.complete:
    task.complete = False
    task.save()
  else:
    task.complete = True
    task.save()
  return redirect('/todo/foodplan/'+str(task.foodplan))


def create_shoppinglist(request, foodplan_id):
  foodplan_recipies = Foodplans.objects.filter(foodplan_id=foodplan_id)
  ingredient_list = []
  for recipe in foodplan_recipies:
    recipe_ingredients = RecipeIngredients.objects.filter(recipe_id=recipe.recipe_id)
    for ingredient in recipe_ingredients:
      ingredient_list.append({
        'name': ingredient.get_ingredient_name(),
        'ingredient_description': ingredient.get_ingredient_description(),
        'ingredient_id': ingredient.ingredient_id,
        'ingredient_category': ingredient.get_ingredient_category(),
        'unit': ingredient.measurement_unit.id, 
        'unit_name':ingredient.get_unit_name(), 
        'amount': ingredient.amount,
        'recipe_ingredient_description': ingredient.description
        })

  # Consolidate ingredient list
  consolidated_list = []
  for ingredient_dict in ingredient_list:
    # check whether an entry with same ingredient_id is present in the compiled list
    check_list = [(i, d) for i, d in enumerate(consolidated_list) if d['ingredient_id'] == ingredient_dict['ingredient_id']]
    # if a match is found
    if check_list:
      for c_i, check in enumerate(check_list):
        index = check[0]  # index of found entry match
        # check if same measurement unit is used
        if consolidated_list[index]['unit'] == ingredient_dict['unit']:
          amount = ingredient_dict['amount']
          old_amount = consolidated_list[index]['amount']
          consolidated_list[index]['amount'] = old_amount + amount
          break
        else:
          # conversion is needed
          amount = convert_amount(ingredient_dict['unit'], consolidated_list[index]['unit'], ingredient_dict['amount'])
          # if conversion is possible
          if amount:
            old_amount = consolidated_list[index]['amount']
            consolidated_list[index]['amount'] = old_amount + amount
            break
          # if not create a separate instance on that ingredient in list
          else:
            # but only if all instances has been checked to see if conversion is possible
            if len(check_list) == c_i+1:
              consolidated_list.append(ingredient_dict)
    else:
      consolidated_list.append(ingredient_dict)
      
  # Create shoppinglist
  for ingredient in consolidated_list:
    shopping_text = ''
    # unit name
    if ingredient['unit'] == 1:
      unit = ''
    else:
      unit = str(ingredient['unit_name'])
    # ingredient description
    if ingredient['ingredient_description']:
      ingredient_description = str(ingredient['ingredient_description'])
    else:
      ingredient_description = ''
    # recipe ingredient description
    if ingredient['recipe_ingredient_description']:
      recipe_ingredient_description = str(ingredient['recipe_ingredient_description'])
    else:
      recipe_ingredient_description = ''
    # amount
    if ingredient['amount'].is_integer():
      amount = str(int(ingredient['amount']))
    else:
      amount = str(ingredient['amount'])
    # Make string
    shopping_text = amount + '' + unit + ' ' + str(ingredient['name']) + ' ' + ingredient_description + ' ' + recipe_ingredient_description
    # Make db entry
    shopping_task = Task(title=shopping_text, ingredient_category=ingredient['ingredient_category'], foodplan=foodplan_id)
    shopping_task.save()
  
  # Mark foodplan as compete (disables editing)
  status = FoodplanStatus(pk=foodplan_id)
  status.complete = True
  status.save()

  return redirect('/todo/foodplan/'+str(foodplan_id))