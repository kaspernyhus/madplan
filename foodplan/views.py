from django.shortcuts import render

def view_foodplans(request):
    return render(request, 'pages/foodplans.html')

def create_foodplan(request):
    return render(request, 'pages/new_foodplan.html')