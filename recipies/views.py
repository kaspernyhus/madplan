from django.shortcuts import render
from .models import *


def show_recipies(request):
    all_recipies = Recipies.objects.all()
    
    recipies = []
    for recipe in all_recipies:
        recipies.append({'name': recipe.name, 'type': recipe.get_type()})
    
    context = {'recipies': recipies}
    return render(request, 'recipies/index.html', context)
