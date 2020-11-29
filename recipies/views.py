from django.shortcuts import render

def show_recipies(request):
    return render(request, 'recipies/index.html')
