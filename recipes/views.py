from django.shortcuts import render, redirect
from .models import Recipe, RecipeComment
from . import forms as recipeforms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from slugify import slugify
from datetime import datetime


# Create your views here.


def recipe_homepage(request):
    return render(request, 'recipes/recipes_homepage.html')


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_list.html',
                  {
                      'recipes': recipes
                  })


def recipe_details(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    comments = RecipeComment.objects.filter(recipe=recipe)
    comment_form = recipeforms.RecipeCommentForm()
    return render(request, 'recipes/recipes_details.html',
                  {
                      'recipe': recipe,
                      'comments': comments,
                      'comment_form': comment_form,
                      'request': request
                  })


@login_required(login_url="accounts:login")
def recipe_create(request):
    if request.method == 'POST':
        recipe_form = recipeforms.RecipeCreateForm(request.POST, request.FILES)
        cost_form = recipeforms.RecipeCostForm(request.POST)
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
        recipe_form = recipeforms.RecipeCreateForm()
        cost_form = recipeforms.RecipeCostForm()
    return render(request, 'recipes/recipes_create.html',
                  {
                      'recipe_create_form': recipe_form,
                      'recipe_cost_form': cost_form
                  })


@login_required(login_url="accounts:login")
def recipe_edit(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if recipe.author == request.user:
        image_form = recipeforms.RecipeImageForm()
        step_form = recipeforms.RecipeStepForm()
        ingred_form = recipeforms.RecipeIngredientForm()
        if request.POST:
            edit_form = recipeforms.RecipeEditForm(request.POST, request.FILES, instance=recipe)
            cost_form = recipeforms.RecipeCostForm(request.POST, instance=recipe.recipe_cost)
            if edit_form.is_valid() and cost_form.is_valid():
                # save recipe to db
                recipe = edit_form.save(commit=False)
                recipe.updated_at = datetime.now()
                recipe.save()
                cost_form.save()
                messages.success(request, "Recipe updated successfully")
                return redirect('recipes:edit', recipe_slug=recipe.slug)
        else:
            edit_form = recipeforms.RecipeEditForm(instance=recipe)
            cost_form = recipeforms.RecipeCostForm(instance=recipe.recipe_cost)
    else:
        messages.error(request, "You're not the author of this recipe")
        return redirect('recipes:homepage')
    return render(request, 'recipes/recipe_edit.html',
                  {
                      'edit_recipe_form': edit_form,
                      'cost_form': cost_form,
                      'image_form': image_form,
                      'step_form': step_form,
                      'ingred_form': ingred_form,
                      'recipe': recipe
                  })


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


@login_required(login_url="accounts:login")
def recipe_add_image(request, recipe_pk):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if recipe.author == request.user:
            image_form = recipeforms.RecipeImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                recipe_image = image_form.save(commit=False)
                recipe_image.recipe = recipe
                recipe_image.save()
                recipe.updated_at = datetime.now()
                recipe.save()
                messages.success(request, 'The image was added successfully')
            return redirect('recipes:edit', recipe_slug=recipe.slug)
        else:
            messages.error(request, "You're not the author of this recipe")
    return redirect('recipes:homepage')


@login_required(login_url="accounts:login")
def recipe_add_step(request, recipe_pk):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if recipe.author == request.user:
            step_form = recipeforms.RecipeStepForm(request.POST)
            if step_form.is_valid():
                recipe_step = step_form.save(commit=False)
                recipe_step.recipe = recipe
                recipe_step.save()
                recipe.updated_at = datetime.now()
                recipe.save()
                messages.success(request, 'The step was added successfully')
            return redirect('recipes:edit', recipe_slug=recipe.slug)
        else:
            messages.error(request, "You're not the author of this recipe")
    return redirect('recipes:homepage')


@login_required(login_url="accounts:login")
def recipe_add_ingredient(request, recipe_pk):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if recipe.author == request.user:
            ingred_form = recipeforms.RecipeIngredientForm(request.POST)
            if ingred_form.is_valid():
                recipe_ingred = ingred_form.save(commit=False)
                recipe_ingred.recipe = recipe
                recipe_ingred.save()
                recipe.updated_at = datetime.now()
                recipe.save()
                messages.success(request, 'The ingredient was added successfully')
            return redirect('recipes:edit', recipe_slug=recipe.slug)
        else:
            messages.error(request, "You're not the author of this recipe")
    return redirect('recipes:homepage')


@login_required(login_url="accounts:login")
def recipe_add_comment(request, recipe_pk):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        comment_form = recipeforms.RecipeCommentForm(request.POST)
        if comment_form.is_valid():
            recipe_comment = comment_form.save(commit=False)
            recipe_comment.recipe = recipe
            recipe_comment.user = request.user
            recipe_comment.save()
            messages.success(request, 'The comment was added successfully')
        return redirect('recipes:details', recipe_slug=recipe.slug)
    return redirect('recipes:homepage')
