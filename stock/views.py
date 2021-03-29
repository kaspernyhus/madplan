from django.shortcuts import render, redirect
from .models import *
from .forms import *


def index(request):
  freezer_items = Freezerstock.objects.all()
  context={'freezer_items':freezer_items}
  return render(request, 'stock/freezerstock.html', context)


def create_freezer_item(request):
  form = FreezerstockForm()
  return render(request, 'stock/freezerstock.html')