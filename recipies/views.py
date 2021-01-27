from django.shortcuts import render, redirect
from .models import *
from .forms import EditRecipeNameForm, NewRecipeForm, RecipeTypeFilterBox, RecipeTagsForm
from recipies.models import Recipies, RecipeTags
from datetime import datetime
from django.utils import timezone
from random import shuffle
from django.db.models import Q


def show_recipies(request):
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
    elif request.GET.get('search_box'):
        search_query = request.GET.get('search_box')
        search_quaries = search_query.split()
        recipies_query = Recipies.objects.filter(Q(name__contains=search_query) | Q(description__contains=search_query))
        # if search is more than one word, make a db quary pr word and OR into quaryset
        for quary in search_quaries:
            _recipies_query = Recipies.objects.filter(Q(name__contains=quary) | Q(description__contains=quary))
            recipies_query |= _recipies_query
        form = RecipeTypeFilterBox()
    else:
        recipies_query = Recipies.objects.all()
        form = RecipeTypeFilterBox()
    recipies = []
    for recipe in recipies_query:
        recipies.append({
            'id':recipe.id, 
            'name': recipe.name, 
            'type': recipe.get_type(), 
            'description': recipe.description, 
            'photo_thumbnail': recipe.photo_thumbnail,
            'prep_time': recipe.prep_time
            })
    # Randomize recipies order
    shuffle(recipies)

    context = {'recipies': recipies, 'form': form}
    return render(request, 'recipies/index.html', context)


def show_recipe(request, recipe_id, qty_multiplier=1.0):
    # Qty multiplier
    if request.method == 'GET':
        if request.GET.getlist('qtymultiplier'):
            qty_multiplier = request.GET.getlist('qtymultiplier')
            qty_multiplier = float(qty_multiplier[0])
    # Get recipe data
    recipe = Recipies.objects.get(pk=recipe_id)
    # for data in recipe_data:
    #     recipe = {
    #         'id': data.id, 
    #         'name': data.name, 
    #         'date': data.date, 
    #         'description': data.description, 
    #         'photo_thumbnail': data.photo_thumbnail,
    #         'qty_multiply': qty_multiplier
    #         }

    # Get recipe ingredients
    recipe_ingredients = RecipeIngredients.objects.all().filter(recipe_id=recipe_id)
    recipe_headers = RecipeIngredientsHeading.objects.all().filter(recipe_id=recipe_id)
    ingredients = []
    for ingredient in recipe_ingredients:
        ingredients.append({
            'name': ingredient.get_ingredient_name(), 
            'description': ingredient.get_ingredient_description(),
            'unit': ingredient.get_unit_name(), 
            'amount': ingredient.amount * qty_multiplier,
            'recipe_ingredient_description': ingredient.description
            })
    # Insert recipe ingredient headers
    recipe_headers = RecipeIngredientsHeading.objects.all().filter(recipe_id=recipe_id)
    for offset, rec_head in enumerate(recipe_headers):
        ingredients.insert(rec_head.place+offset, {'heading':rec_head.heading})

    recipe_instructions = RecipeInstructions.objects.all().filter(recipe_id=recipe_id)

    context = {'recipe': recipe, 'ingredients': ingredients, 'instructions': recipe_instructions}
    return render(request, 'recipies/recipe.html', context)


def new_recipe(request):
    if request.method == 'POST':
        form = NewRecipeForm(request.POST, request.FILES)
        if form.is_valid:
            new_recipe = form.save()
        return redirect('/recipies/edit/'+str(new_recipe.pk))

    form = NewRecipeForm()
    return render(request, 'recipies/new_recipe.html', {'form': form})


def edit_recipe(request, recipe_id):
    if request.method == 'POST':
        if request.POST.getlist('delete_ingredient'):
            RecipeIngredient_id = request.POST.getlist('delete_ingredient')
            RecipeIngredient_id = int(RecipeIngredient_id[0])
            ingredient = RecipeIngredients.objects.get(pk=RecipeIngredient_id)
            ingredient.delete()
            # Update changes date for recipe
            recipe = Recipies.objects.get(pk=recipe_id)
            recipe.date = timezone.now()
            recipe.save()
        elif request.POST.getlist('add_ingredient'):
            # Get str value from html datalist and split to get id to be able to search db
            ingredient_id_POST = request.POST.getlist('ingredient')
            ingredient_id_name = ingredient_id_POST[0].split(':') # seperate by ':'
            # if 'id:' present
            if len(ingredient_id_name) == 2:
                ingredient_id = ingredient_id_name[0]
                ingredient_name = ingredient_id_name[1].strip()
            # if not propably a user input = new ingredient
            else:
                ingredient_id = 0
                ingredient_name = ingredient_id_name[0]
            # Try to get object from db
            try:
                ingredient_query = Ingredients.objects.get(pk=ingredient_id)
            # if not found in data base create new ingredient
            except:
                next_path = request.path
                return redirect('/ingredients/new_ingredient?next='+next_path+'&ing_name='+ingredient_name)
            # Get values from other form fields
            recipe_ingredient_description = request.POST.getlist('description')
            ingredient_quantity = request.POST.getlist('qty')
            ingredient_unit = request.POST.getlist('qty_unit')
            ingredient_unit_id = MeasurementUnits.objects.get(unit_name=ingredient_unit[0])
            # Make new db entry with entered data
            ingredient_to_add = RecipeIngredients(
                recipe_id=recipe_id, ingredient_id=ingredient_query.id, 
                measurement_unit=ingredient_unit_id, 
                amount=ingredient_quantity[0], 
                description=recipe_ingredient_description[0]
                )
            ingredient_to_add.save()
            # Update changes date for recipe
            recipe = Recipies.objects.get(pk=recipe_id)
            recipe.date = timezone.now()
            recipe.save()
        elif request.POST.get('delete_heading'):
            rec_ing_head_id = request.POST.get('delete_heading')
            recipe_heading = RecipeIngredientsHeading.objects.get(pk=rec_ing_head_id)
            recipe_heading.delete()
        elif request.POST.get('heading'):
            heading = request.POST.get('heading')
            ingredients_num = request.POST.getlist('recipe_ingredient_id')
            place = len(ingredients_num)
            add_heading = RecipeIngredientsHeading(recipe_id=recipe_id, heading=heading, place=place)
            add_heading.save()
        elif request.POST.getlist('edit_quantities'):
            recipe_ingredients_ids = request.POST.getlist('recipe_ingredient_id')
            quantities = request.POST.getlist('qty')
            for i, recipe_ingredient_id in enumerate(recipe_ingredients_ids):
                ingredient = RecipeIngredients.objects.get(pk=recipe_ingredient_id)
                ingredient.amount = quantities[i]
                ingredient.save()
            # Update changes date for recipe
            recipe = Recipies.objects.get(pk=recipe_id)
            recipe.date = timezone.now()
            recipe.save()
        elif request.POST.getlist('edit_instructions'):
            recipe_instructions_query = RecipeInstructions.objects.all().filter(recipe_id=recipe_id)
            instructions = request.POST.getlist('textarea_instructions')
            new_instruction = request.POST.getlist('new_instruction')
            step = 0
            # Update existing instructions
            for i, rec_inst_object in enumerate(recipe_instructions_query):
                rec_inst_object.description = instructions[i]
                rec_inst_object.save()
                step = i
            # Add new instruction
            if new_instruction[0] is not '':
                new_isbold = request.POST.getlist('new_isbold')
                if not new_isbold:
                    new_isbold = False
                else:
                    new_isbold = True
                next_step = step+1
                new_line = RecipeInstructions(recipe_id=recipe_id, step=next_step, description=new_instruction[0], is_bold=new_isbold)
                new_line.save()
            # Edit is_bold
            is_bold = request.POST.getlist('isbold')
            is_bold = [int(i) for i in is_bold] 
            for rec_inst_object in recipe_instructions_query:
                if rec_inst_object.id in is_bold:
                    rec_inst_object.is_bold = True
                else:
                    rec_inst_object.is_bold = False
                rec_inst_object.save()
            # Update changed date for recipe
            recipe = Recipies.objects.get(pk=recipe_id)
            recipe.date = timezone.now()
            recipe.save()
        elif request.POST.getlist('edit_tags'):
            tags = request.POST.getlist('tags')
            prep_time = request.POST.get('prep_time')
            new_URL = request.POST.get('URL')
            recipe = Recipies.objects.get(pk=recipe_id)
            recipe.tags.set(tags)
            recipe.prep_time = prep_time
            recipe.URL = new_URL
            recipe.save()

    
    # Get recipe data
    recipe_data = Recipies.objects.get(pk=recipe_id)
    # recipe_data = []
    # for data in recipe_data_quary:
    #     recipe_data = {
    #         'id': data.id, 
    #         'name': data.name, 
    #         'date': data.date, 
    #         'description': data.description, 
    #         'photo_thumbnail': data.photo_thumbnail, 
    #         'tags': data.tags,
    #         'prep_time': data.prep_time
    #         }
    # Get info on the ingredients in the recipe
    recipe_ingredients_quary = RecipeIngredients.objects.all().filter(recipe_id=recipe_id)
    recipe_ingredients = []
    for ingredient in recipe_ingredients_quary:
        recipe_ingredients.append({
            'id': ingredient.id,
            'ingredients_id': ingredient.ingredient_id,
            'name': ingredient.get_ingredient_name(), 
            'description': ingredient.get_ingredient_description(), 
            'unit': ingredient.get_unit_name(), 
            'amount': ingredient.amount,
            'recipe_ingredient_description': ingredient.description
            })
    # Insert recipe ingredient headers
    recipe_headers = RecipeIngredientsHeading.objects.all().filter(recipe_id=recipe_id)
    for offset, rec_head in enumerate(recipe_headers):
        recipe_ingredients.insert(rec_head.place+offset, {'heading':rec_head})
    # Get recipe instructions
    recipe_instructions = RecipeInstructions.objects.all().filter(recipe_id=recipe_id)
    # Get a list of all avaiable ingredients
    all_ingredients_quary = Ingredients.objects.all().order_by('name')
    # Get a list of all measurement unit options
    units = MeasurementUnits.objects.all()
    # Tags form
    tags_query = RecipeTags.objects.all().filter(recipies=recipe_id)
    tags = [object.id for object in tags_query]
    form = RecipeTagsForm(initial={'tags':tags, 'prep_time': recipe_data.prep_time, 'URL': recipe_data.URL})

    context = {'recipe': recipe_data, 'recipe_ingredients': recipe_ingredients, 'instructions': recipe_instructions, 'all_ingredients': all_ingredients_quary, 'units': units, 'form': form}
    return render(request, 'recipies/edit_recipe.html', context)


def edit_recipe_name(request, recipe_id):
    recipe = Recipies.objects.get(pk=recipe_id)

    if request.method == 'POST':
        form = EditRecipeNameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            recipe.name = name
            recipe.description = description
            recipe.save()
        return redirect('/recipies/edit/'+str(recipe_id))

    form = EditRecipeNameForm(initial={'name':recipe.name, 'description': recipe.description})
    return render(request, 'recipies/edit_name.html', {'form': form})
