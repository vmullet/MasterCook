from django.shortcuts import render

# Create your views here.


def recipe_list(request):
    return render(request, 'recipes/index.html')


def recipe_details(request,id):
    return render(request, 'recipes/details.html', {'id': id})
