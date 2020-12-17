from django.shortcuts import render
from foodplan.models import Foodplans
from .models import Task



def index(request):
  foodplans = Foodplans.objects.all()

  context = {'foodplans': foodplans}
  return render(request, 'todo/index.html', context)


def view_shoppinglist(request):
  tasks = Task.objects.all().filter(foodplan=1)

  context = {'tasks': tasks}
  return render(request, 'todo/shoppinglist.html', context)