from django.shortcuts import render, redirect
from .models import Recipe
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.


def recipe_homepage(request):
    return render(request, 'recipes/recipes_homepage.html')


def recipe_list(request):
    return render(request, 'recipes/recipes_list.html')


def recipe_details(request, recipe):
    # recipe = Recipe.objects.get(slug=slug)
    return render(request, 'recipes/recipes_details.html', {'recipe': recipe})


@login_required(login_url="accounts:login")
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


@login_required(login_url="accounts:login")
def recipe_edit(request, recipe_pk):
    pass


@login_required(login_url="accounts:login")
def recipe_delete(request, recipe_pk):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if recipe.author == request.user:
            recipe.delete()
            messages.success(request, 'Recipe was deleted successfully')
        else:
            messages.error(request, "You're not the author of this recipe")
    return redirect('recipes:homepage')
