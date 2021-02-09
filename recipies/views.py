from django.shortcuts import render, redirect
from .models import *
from .forms import AddAddonsForm, AddonActiveForm, EditRecipeIngredientForm, EditRecipeNameForm, NewRecipeForm, RecipeTypeFilterBox, RecipeTagsForm
from recipies.models import Recipies, RecipeTags
from datetime import datetime
from django.utils import timezone
from random import shuffle
from django.db.models import Q
from django.forms.formsets import formset_factory


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
        recipies_query = Recipies.objects.filter(tags=filter_by).exclude(Q(recipe_type=2)|Q(recipe_type=9)) # exclude 'Tilbehør', 'Andet'
        form = RecipeTypeFilterBox(initial={'tags': filter_by})
    elif request.GET.get('search_box'):
        search_query = request.GET.get('search_box')
        search_quaries = search_query.split()
        # Search recipies name and description
        recipies_query = Recipies.objects.filter(Q(name__contains=search_query) | Q(description__contains=search_query))
        # Search for recipies with ingredient names
        ingredient_name_ids = Ingredients.objects.filter(name__contains=search_query)
        for ingredient_name_id in ingredient_name_ids:
            ingredients_query = RecipeIngredients.objects.filter(ingredient_id=ingredient_name_id)
            for recipe_ingredient in ingredients_query:
                _recipies_query = Recipies.objects.filter(pk=recipe_ingredient.recipe_id)
                recipies_query |= _recipies_query
        # if search is more than one word, make a db quary pr word and OR into quaryset
        for quary in search_quaries:
            _recipies_query = Recipies.objects.filter(Q(name__contains=quary) | Q(description__contains=quary))
            recipies_query |= _recipies_query
        form = RecipeTypeFilterBox()
    else:
        recipies_query = Recipies.objects.all().exclude(Q(recipe_type=2)|Q(recipe_type=9)) # exclude 'Tilbehør', 'Andet'
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
    if request.method == 'POST':
        print('--------------------')
        print(request.POST)
        print('--------------------')
        # Delete add_on recipe
        if request.POST.get('delete_add_on'):
            add_on_id = request.POST.get('delete_add_on')
            add_on = AddOns.objects.get(pk=add_on_id)
            add_on.delete()
        # Add add-on recipies
        form = AddAddonsForm(request.POST)
        if form.is_valid():
            add_on_id = form.cleaned_data['add_on']
            recipe = Recipies.objects.get(pk=recipe_id)
            adding = AddOns(recipe=recipe, add_on=add_on_id)
            adding.save()
        # Add_on active state change
        if request.POST.get('add-on-active-changed'):
            add_on_active_changed = request.POST.get('add-on-active-changed')
            add_on_active = request.POST.getlist('add-on-active')
            add_on = AddOns.objects.get(pk=add_on_active_changed)
            if add_on_active_changed in add_on_active:
                add_on.active = True
                add_on.save()
            else:
                add_on.active = False
                add_on.save()
        if request.POST.get('add-on-qtymultiplier'):
            add_on_qty = request.POST.get('add-on-qtymultiplier')
            add_on_id = request.POST.get('add-on-qtymultiplier_id')
            add_on = AddOns.objects.get(pk=add_on_id)
            add_on.qty_multiplier = add_on_qty
            add_on.save()

    # Qty multiplier
    if request.method == 'GET':
        if request.GET.getlist('qtymultiplier'):
            qty_multiplier = request.GET.getlist('qtymultiplier')
            qty_multiplier = float(qty_multiplier[0])
        
    # Get recipe data
    recipe = Recipies.objects.get(pk=recipe_id)
    # Get recipe ingredients
    recipe_ingredients = RecipeIngredients.objects.all().filter(recipe_id=recipe_id)
    recipe_headers = RecipeIngredientsHeading.objects.all().filter(recipe_id=recipe_id)
    ingredients = []
    for ingredient in recipe_ingredients:
        amount = ingredient.amount * qty_multiplier
        if amount.is_integer():
            amount = int(amount)
        else:
            amount = round(amount, 2)
        ingredients.append({
            'id': ingredient.id,
            'name': ingredient.get_ingredient_name(), 
            'description': ingredient.get_ingredient_description(),
            'unit': ingredient.measurement_unit, 
            'amount': amount,
            'recipe_ingredient_description': ingredient.description
            })
    # Insert recipe ingredient headers
    recipe_headers = RecipeIngredientsHeading.objects.filter(recipe_id=recipe_id)
    for offset, rec_head in enumerate(recipe_headers):
        ingredients.insert(rec_head.place+offset, {'heading':rec_head.heading})
    recipe_instructions = RecipeInstructions.objects.filter(recipe_id=recipe_id)
    # Get Add-ons
    form = AddAddonsForm()
    add_on_recipies = []
    if recipe.add_ons:
        add_ons = AddOns.objects.filter(recipe=recipe.id)
        for add_on in add_ons:
            add_on_recipe = Recipies.objects.get(pk=add_on.add_on_id)
            add_on_recipe_ingredients = RecipeIngredients.objects.filter(recipe_id=add_on_recipe.id)
            add_on_recipies.append({'add_on': add_on, 'recipe': add_on_recipe, 'recipe_ingredients': add_on_recipe_ingredients, 'form': AddonActiveForm(initial={'add_on_active': add_on.active})})

    context = {'recipe': recipe, 'add_ons': add_on_recipies, 'ingredients': ingredients, 'instructions': recipe_instructions, 'qty_multiplier': qty_multiplier, 'form': form}
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
    # print('--------------------')
    # print(request.POST)
    # print('--------------------')
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
        if request.POST.getlist('add_ingredient'):
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
        if request.POST.get('delete_heading'):
            rec_ing_head_id = request.POST.get('delete_heading')
            recipe_heading = RecipeIngredientsHeading.objects.get(pk=rec_ing_head_id)
            recipe_heading.delete()
        if request.POST.get('heading'):
            heading = request.POST.get('heading')
            ingredients_num = request.POST.getlist('recipe_ingredient_id')
            place = len(ingredients_num)
            add_heading = RecipeIngredientsHeading(recipe_id=recipe_id, heading=heading, place=place)
            add_heading.save()
        if request.POST.getlist('edit_quantities'):
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
        if request.POST.getlist('edit_instructions'):
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
        if request.POST.getlist('edit_tags'):
            form = RecipeTagsForm(request.POST)
            if form.is_valid():
                recipe_type = request.POST.get('recipe_type')
                recipe_type_obj = RecipeTypes.objects.get(pk=recipe_type)
                tags = request.POST.getlist('tags')
                new_URL = request.POST.get('URL')
                allow_add_ons = form.cleaned_data['add_ons']
                preferred_add_ons = form.cleaned_data['preferred_add_ons']
                recipe = Recipies.objects.get(pk=recipe_id)
                recipe.tags.set(tags)
                recipe.URL = new_URL
                recipe.add_ons = allow_add_ons
                recipe.recipe_type = recipe_type_obj
                recipe.preferred_add_ons.set(preferred_add_ons)
                recipe.save()
    # Get recipe data
    recipe_data = Recipies.objects.get(pk=recipe_id)
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
    preferred_query = Recipies.objects.filter(preferred_add_ons=recipe_id)
    preferred = [object.id for object in preferred_query]
    form = RecipeTagsForm(preferred_field=recipe_data.add_ons, initial={'recipe_type': recipe_data.recipe_type, 
                                                                        'tags':tags, 
                                                                        'URL': recipe_data.URL, 
                                                                        'add_ons': recipe_data.add_ons,
                                                                        'preferred_add_ons': preferred
                                                                        })
    context =  {'recipe': recipe_data, 
                'recipe_ingredients': recipe_ingredients, 
                'instructions': recipe_instructions, 
                'all_ingredients': all_ingredients_quary, 
                'units': units, 
                'form': form}

    return render(request, 'recipies/edit_recipe.html', context)


def edit_recipe_name(request, recipe_id):
    recipe = Recipies.objects.get(pk=recipe_id)
    if request.method == 'POST':
        form = EditRecipeNameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            prep_time = form.cleaned_data['prep_time']
            recipe.name = name
            recipe.description = description
            recipe.prep_time = prep_time
            recipe.save()
        return redirect('/recipies/edit/'+str(recipe_id))

    form = EditRecipeNameForm(initial={'name':recipe.name, 'description': recipe.description, 'prep_time': recipe.prep_time})
    return render(request, 'recipies/edit_name.html', {'form': form})


def edit_reciep_ingredient(request, recipe_ingredient_id):
    recipe_ingredient = RecipeIngredients.objects.get(pk=recipe_ingredient_id)
    if request.method == 'POST':
        form = EditRecipeIngredientForm(request.POST)
        if form.is_valid():
            recipe_ingredient.ingredient = form.cleaned_data['ingredient']
            recipe_ingredient.description = form.cleaned_data['description']
            recipe_ingredient.amount = form.cleaned_data['amount']
            recipe_ingredient.measurement_unit = form.cleaned_data['measurement_unit']
            recipe_ingredient.save()
            return redirect('/recipies/'+str(recipe_ingredient.recipe_id))
    edit_ingredient_form = EditRecipeIngredientForm(initial={'ingredient': recipe_ingredient.ingredient_id,'description': recipe_ingredient.description, 'amount': recipe_ingredient.amount, 'measurement_unit': recipe_ingredient.measurement_unit})
    print(recipe_ingredient.measurement_unit)
    print(edit_ingredient_form)
    return render(request, 'recipies/edit_recipe_ingredient.html', {'form': edit_ingredient_form})


def delete_recipe(request, recipe_id):
    recipe = Recipies.objects.get(pk=recipe_id)
    recipe.delete()
    return redirect('/')