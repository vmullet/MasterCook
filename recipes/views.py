from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeCreateForm, RecipeCostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from slugify import slugify

# Create your views here.


def recipe_homepage(request):
    return render(request, 'recipes/recipes_homepage.html')


def recipe_list(request):
    return render(request, 'recipes/recipes_list.html')


def recipe_details(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    return render(request, 'recipes/recipes_details.html', {'recipe': recipe})


@login_required(login_url="accounts:login")
def recipe_create(request):
    if request.method == 'POST':
        recipe_form = RecipeCreateForm(request.POST, request.FILES)
        cost_form = RecipeCostForm(request.POST)
        if recipe_form.is_valid() and cost_form.is_valid():
            # save recipe to db
            recipe = recipe_form.save(commit=False)
            recipe.slug = slugify(recipe.name)
            recipe_cost = cost_form.save()
            recipe.recipe_cost = recipe_cost
            recipe.author = request.user
            recipe.save()
            return redirect('recipes:edit', recipe_slug=recipe.slug)
    else:
        recipe_form = RecipeCreateForm()
        cost_form = RecipeCostForm()
    return render(request, 'recipes/recipes_create.html',
                  {
                      'recipe_create_form': recipe_form,
                      'recipe_cost_form': cost_form
                   })


@login_required(login_url="accounts:login")
def recipe_edit(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if recipe.author == request.user:
        if request.POST:
            pass
        else:
            pass
    else:
        messages.error(request, "You're not the author of this recipe")
        return redirect('recipes:homepage')
    return render(request, 'recipes/recipe_edit.html')


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
