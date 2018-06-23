from django.shortcuts import render, redirect
from .models import Recipe
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.


def recipe_homepage(request):
    return render(request, 'recipes/recipes_homepage.html')


def recipe_list(request):
    return render(request, 'recipes/recipes_list.html')


def recipe_details(request, recipe):
    # recipe = Recipe.objects.get(slug=slug)
    return render(request, 'recipes/recipes_details.html', {'recipe': recipe})


@login_required(login_url="/accounts/login/")
def recipe_create(request):
    if request.method == 'POST':
        form = forms.CreateRecipe(request.POST, request.FILES)
        if form.is_valid():
            # save recipe to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('recipes:list')
    else:
        form = forms.CreateRecipe()
    return render(request, 'recipes/recipes_create.html', {'form': form})


