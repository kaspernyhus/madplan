from django.shortcuts import render, redirect
from .models import *
from .forms import NewRecipeForm, RecipeTypeFilterBox, RecipeTagsForm
from recipies.models import Recipies, RecipeTags
from datetime import datetime
from django.utils import timezone


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
    else:
        recipies_query = Recipies.objects.all()
        form = RecipeTypeFilterBox()
    
    
    recipies = []
    for recipe in recipies_query:
        recipies.append({'id':recipe.id, 'name': recipe.name, 'type': recipe.get_type(), 'description': recipe.description, 'photo_thumbnail': recipe.photo_thumbnail})
    
    context = {'recipies': recipies, 'form': form}
    return render(request, 'recipies/index.html', context)


def show_recipe(request, recipe_id):
    # Get recipe data
    recipe_data = Recipies.objects.all().filter(pk=recipe_id)
    for data in recipe_data:
        recipe = {'id': data.id, 'name': data.name, 'date': data.date, 'description': data.description, 'photo_thumbnail': data.photo_thumbnail}

    # Get recipe ingredients
    recipe_ingredients = RecipeIngredients.objects.all().filter(recipe_id=recipe_id)
    ingredients = []
    for ingredient in recipe_ingredients:
        ingredients.append({
            'name': ingredient.get_ingredient_name(), 
            'unit': ingredient.get_unit_name(), 
            'amount': ingredient.amount, 
            'description': ingredient.get_ingredient_description() 
            })
    
    recipe_instructions = RecipeInstructions.objects.all().filter(recipe_id=recipe_id)

    context = {'recipe': recipe, 'ingredients': ingredients, 'instructions': recipe_instructions}
    return render(request, 'recipies/recipe.html', context)


def new_recipe(request):
    if request.method == 'POST':
        form = NewRecipeForm(request.POST, request.FILES)
        if form.is_valid:
            new_recipe = form.save()
            print(new_recipe.tags)
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
            # Get value (name) from dropdown and split to be able to search db
            ingredient_name_POST = request.POST.getlist('ingredient')
            ingredient_name = [name.strip() for name in ingredient_name_POST[0].split(',')]
            # Get id of ingredient name from db
            try:
                ingredient_query = Ingredients.objects.get(name=ingredient_name[0])
            # if not found in data base create new ingredient
            except:
                next_path = request.path
                return redirect('/ingredients/new_ingredient?next='+next_path+'&ing_name='+ingredient_name[0])
            # Get values from other form fields
            ingredient_quantity = request.POST.getlist('qty')
            ingredient_unit = request.POST.getlist('qty_unit')
            ingredient_unit_id = MeasurementUnits.objects.get(unit_name=ingredient_unit[0])
            # Make new db entry with entered data
            ingredient_to_add = RecipeIngredients(recipe_id=recipe_id, ingredient_id=ingredient_query.id, measurement_unit=ingredient_unit_id, amount=ingredient_quantity[0])
            ingredient_to_add.save()
            # Update changes date for recipe
            recipe = Recipies.objects.get(pk=recipe_id)
            recipe.date = timezone.now()
            recipe.save()
        elif request.POST.getlist('edit_quantities'):
            ingredient_ids = request.POST.getlist('ingredient_id')
            quantities = request.POST.getlist('qty')
            for i, ingredient_id in enumerate(ingredient_ids):
                ingredient = RecipeIngredients.objects.get(recipe_id=recipe_id, ingredient=ingredient_id)
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
            # Update existing
            for i, rec_inst_object in enumerate(recipe_instructions_query):
                rec_inst_object.description = instructions[i]
                rec_inst_object.save()
                step = i
            if new_instruction[0] is not '':
                next_step = step+1
                new_line = RecipeInstructions(recipe_id=recipe_id, step=next_step, description=new_instruction[0])
                new_line.save()
            # Update changes date for recipe
            recipe = Recipies.objects.get(pk=recipe_id)
            recipe.date = timezone.now()
            recipe.save()
        elif request.POST.getlist('edit_tags'):
            tags = request.POST.getlist('tags')
            recipe = Recipies.objects.get(pk=recipe_id)
            recipe.tags.set(tags)
            recipe.save()

    
    # Get recipe data
    recipe_data = Recipies.objects.all().filter(pk=recipe_id)
    for data in recipe_data:
        recipe = {'id': data.id, 'name': data.name, 'date': data.date, 'description': data.description, 'photo_thumbnail': data.photo_thumbnail, 'tags': data.tags}

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
            'amount': ingredient.amount
            })

    # Get recipe instructions
    recipe_instructions = RecipeInstructions.objects.all().filter(recipe_id=recipe_id)

    # Get a list of all avaiable ingredients
    all_ingredients_quary = Ingredients.objects.all()

    # Get a list of all measurement unit options
    units = MeasurementUnits.objects.all()

    # Tags form
    tags_query = RecipeTags.objects.all().filter(recipies=recipe_id)
    tags = [object.id for object in tags_query]
    form = RecipeTagsForm(initial={'tags':tags})

    context = {'recipe': recipe, 'recipe_ingredients': recipe_ingredients, 'instructions': recipe_instructions, 'all_ingredients': all_ingredients_quary, 'units': units, 'form': form }
    return render(request, 'recipies/edit_recipe.html', context)

