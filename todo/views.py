from django.shortcuts import render, redirect
from foodplan.models import Foodplans, FoodplanStatus
from recipies.models import RecipeIngredients, Recipies
from .models import Shoppinglist, Task
from .forms import TaskForm
from unit_conversion.unit_conversion import convert_amount
from datetime import datetime


def index(request):
  shoppinglists_quary = Shoppinglist.objects.all().order_by('-created')
  shoppinglists = []
  for shoppinglist in shoppinglists_quary:
    if shoppinglist.list_source == 'foodplan':
      foodplan_quary = Foodplans.objects.all().filter(foodplan_id=shoppinglist.source_id)
      source_name = 'Madplan ' + foodplan_quary[0].date.strftime("%d/%m/%Y")
    elif shoppinglist.list_source == 'recipe':
      recipe_quary = Recipies.objects.get(pk=shoppinglist.source_id)
      source_name = recipe_quary.name
    else:
      source_name = 'None'
    shoppinglists.append({'quary': shoppinglist, 'source_name': source_name})

  context = {'shoppinglists': shoppinglists}
  return render(request, 'todo/index.html', context)


def view_shoppinglist(request, shoppinglist_id):
  if request.method == 'POST':
    if request.POST.getlist('delete_task'):
        task_id = request.POST.getlist('delete_task')
        task_id = int(task_id[0])
        task = Task.objects.get(pk=task_id)
        task.delete()
    else:
      # add item to shoppinglist
      form = TaskForm(request.POST)
      if form.is_valid:
        form_tosave = form.save(commit=False)
        form_tosave.shoppinglist_id = shoppinglist_id
        form_tosave.save()
  
  tasks_quary = Task.objects.filter(shoppinglist=shoppinglist_id).order_by('ingredient_category__shop_order')
  form = TaskForm()

  # ingredient categories in shoppinglist
  categories = []
  [categories.append(task.ingredient_category) for task in tasks_quary if task.ingredient_category not in categories]

  context = {'tasks': tasks_quary, 'categories': categories, 'form': form}
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
  return redirect('/todo/'+str(task.shoppinglist_id))


def create_shoppinglist(request, id, source):
  # Create shoppinglist entry
  new_shoppinglist = Shoppinglist(list_source=source, source_id=id)
  new_shoppinglist.save()
  ingredient_list = []
  if source == 'foodplan':
    # Mark foodplan as compete (disables editing)
    status = FoodplanStatus(pk=id)
    status.complete = True
    status.save()
    
    foodplan_recipies = Foodplans.objects.filter(foodplan_id=id)
    for recipe in foodplan_recipies:
      recipe_ingredients = RecipeIngredients.objects.filter(recipe_id=recipe.recipe_id)
      for ingredient in recipe_ingredients:
        ingredient_list.append({
          'id': ingredient.ingredient_id,
          'name': ingredient.get_ingredient_name(),
          'ingredient_description': ingredient.get_ingredient_description(),
          'ingredient_id': ingredient.ingredient_id,
          'ingredient_category': ingredient.get_ingredient_category(),
          'unit': ingredient.measurement_unit.id, 
          'unit_name':ingredient.get_unit_name(), 
          'amount': ingredient.amount,
          'recipe_ingredient_description': ingredient.description
          })
  elif source == 'recipe':
    recipe_ingredients = RecipeIngredients.objects.filter(recipe_id=id)
    for ingredient in recipe_ingredients:
        ingredient_list.append({
          'id': ingredient.ingredient_id,
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
    if ingredient['id'] == 49 or ingredient['id'] == 56: # salt
      pass
    else:
      shopping_text = ''
      # unit name
      if ingredient['unit'] == 1:
        unit = ''
      elif ingredient['unit'] < 8:
        unit = str(ingredient['unit_name'])
      else:
        unit = ' ' + str(ingredient['unit_name'])
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
      shopping_text = amount + unit + ' ' + str(ingredient['name']) + ' ' + ingredient_description + ' ' + recipe_ingredient_description
      # Make db entry
      shopping_task = Task(title=shopping_text, ingredient_category=ingredient['ingredient_category'], shoppinglist=new_shoppinglist)
      shopping_task.save()

  return redirect('/todo/'+str(new_shoppinglist.id))