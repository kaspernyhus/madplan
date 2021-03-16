from django.shortcuts import render, redirect
from .forms import *
from recipies.models import AddOns, RecipeIngredients, Recipies

def index(request):
  search_result = []
  # create cache if first time visiting
  try: 
    if not request.session['ingredients']:
      request.session['ingredients'] = []
  except:
    request.session['ingredients'] = []
  # if "forfra" pressed
  if request.method == 'POST':
    print(request.POST)
    if request.POST.get('restart'):
      print('RESTART--------------------')
      request.session['ingredients'] = []
      added_ingredients = []
  else:
    added_ingredients = []
    if request.session['ingredients']:      
      added_ingredients = (request.session['ingredients'])
    if request.GET.get('ingredient'):
      # Get str value from html datalist and split to get id to be able to search db
      ingredient_id_GET = request.GET.getlist('ingredient')
      ingredient_id_name = ingredient_id_GET[0].split(':') # seperate by ':'
      added_ingredients.append({'id': ingredient_id_name[0],'name': ingredient_id_name[1]})
      request.session['ingredients'] = added_ingredients
  
  # find recipies with those ingredients
  if added_ingredients:
    # find where ingredient_id is used in RecipeIngredients, then get Recipies.
    for ingredient in added_ingredients:
      ingredients_query = RecipeIngredients.objects.filter(ingredient_id=ingredient['id'])
      for recipe_ingredient in ingredients_query:
        recipies_query = Recipies.objects.get(pk=recipe_ingredient.recipe_id)
        # if list is empty, add first recipe
        if not search_result:
          search_result.append({'rating': 3, 'recipe_obj': recipies_query})
        else:
          # if recipe is not already in list og search result
          if not any(d['recipe_obj'].id == recipies_query.id for d in search_result):
            search_result.append({'rating': 3, 'recipe_obj': recipies_query})
          else:
            # if recipe is in list give higher rating
            for d in search_result:
                if d['recipe_obj'].id == recipies_query.id:
                    d['rating'] = d['rating']+3
        # find associated recipies where that ingredient is used in an add_on recipe
        add_on_query = AddOns.objects.filter(add_on=recipies_query.id)
        for add_on in add_on_query:
          recipies_query_addon = Recipies.objects.get(pk=add_on.recipe_id)
          if not any(d['recipe_obj'].id == recipies_query_addon.id for d in search_result):
            search_result.append({'rating': 1, 'recipe_obj': recipies_query_addon})
          else:
            for d in search_result:
                if d['recipe_obj'].id == recipies_query_addon.id:
                    d['rating'] = d['rating']+1

  # sort search results after rating, highest first
  search_results = sorted(search_result, key=lambda k: k['rating'], reverse=True) 

  print('--------------------')
  print('Search results: ')
  for i in search_results:
    print(i, i['recipe_obj'].id)
  print('--------------------')

  # Get a list of all avaiable ingredients
  all_ingredients_quary = Ingredients.objects.all().order_by('name')

  context = {'all_ingredients': all_ingredients_quary, 'added_ingredients': added_ingredients, 'found_recipies': search_results}
  return render(request, 'emptyfridge/emptyfridge.html', context)
