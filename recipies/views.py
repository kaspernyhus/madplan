from django.shortcuts import render

def recipies(request):
    return render(request, 'recipies/index.html')
