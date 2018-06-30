from django.shortcuts import render, redirect
from .models import Recipe, RecipeType, RecipeSkill, RecipeComment, RecipeRate, RecipeIngredient, RecipeStep, RecipeImage
from . import forms as recipeforms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from slugify import slugify
from datetime import datetime
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Avg


# Create your views here.

def recipe_homepage(request):
    return render(request, 'recipes/recipes_homepage.html')


def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipes_list.html',
                  {
                      'recipes': recipes
                  })


def recipe_details(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    recipe_steps = RecipeStep.objects.filter(recipe=recipe)
    recipe_photos = RecipeImage.objects.filter(recipe=recipe)
    comments = RecipeComment.objects.filter(recipe=recipe).order_by('-created_at')
    num_page = 1
    if 'num_page' in request.GET:
        num_page = request.GET['num_page']
    paginator = Paginator(comments, settings.MAX_COMMENT_PAGE)
    recipe_rate = None
    if request.user.is_authenticated:
        recipe_rate = RecipeRate.objects.filter(recipe=recipe, user=request.user).first()

    rate_form = recipeforms.RecipeRateForm(instance=recipe_rate)
    comment_form = recipeforms.RecipeCommentForm()
    return render(request, 'recipes/recipes_details.html',
                  {
                      'recipe': recipe,
                      'recipe_ingredients': recipe_ingredients,
                      'recipe_steps': recipe_steps,
                      'recipe_photos': recipe_photos,
                      'comment_paginator': paginator.page(num_page),
                      'current_page': num_page,
                      'range_page': range(1, paginator.num_pages + 1),
                      'number_comments': comments.count,
                      'comment_form': comment_form,
                      'rate_form': rate_form,
                      'user': request.user
                  })


def recipe_search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        recipes = Recipe.objects.filter(name__contains=keyword)
        if 'filter' in request.GET and 'order' in request.GET:
            filt = request.GET['filter']
            order = request.GET['order']
            filterform = recipeforms.RecipeFilterForm(keyword, filt, order)
            if filt == 'recipe_rate':
                results = recipes.annotate(avg_rate=Avg('rates__rate')).order_by(order + 'avg_rate')
            else:
                results = recipes.order_by(order + filt)
        else:
            filterform = recipeforms.RecipeFilterForm(keyword, 'name', '')
            results = recipes.order_by('name')
        return render(request, 'recipes/recipe_search.html', {
            'results': results,
            'keyword': keyword,
            'filterform': filterform
        })
    return redirect('recipes:list')


def recipe_browse_category(request, category_name):
    category = get_object_or_404(RecipeType, name=category_name)
    recipes = Recipe.objects.filter(recipe_type=category)
    keyword = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        recipes = recipes.filter(name__contains=keyword)
    if 'filter' in request.GET and 'order' in request.GET:
        filt = request.GET['filter']
        order = request.GET['order']
        filterform = recipeforms.RecipeFilterForm(keyword, filt, order)
        if filt == 'recipe_rate':
            results = recipes.annotate(avg_rate=Avg('rates__rate')).order_by(order + 'avg_rate')
        else:
            results = recipes.order_by(order + filt)
    else:
        filterform = recipeforms.RecipeFilterForm('', 'name', '')
        results = recipes.order_by('name')
    return render(request, 'recipes/recipe_search.html', {
        'results': results,
        'keyword': keyword,
        'filterform': filterform
    })


def recipe_browse_skill(request, skill_name):
    skill = get_object_or_404(RecipeSkill, name=skill_name)
    recipes = Recipe.objects.filter(recipe_skill=skill)
    keyword = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        recipes = recipes.filter(name__contains=keyword)
    if 'filter' in request.GET and 'order' in request.GET:
        filt = request.GET['filter']
        order = request.GET['order']
        filterform = recipeforms.RecipeFilterForm(keyword, filt, order)
        if filt == 'recipe_rate':
            results = recipes.annotate(avg_rate=Avg('rates__rate')).order_by(order + 'avg_rate')
        else:
            results = recipes.order_by(order + filt)
    else:
        filterform = recipeforms.RecipeFilterForm('', 'name', '')
        results = recipes.order_by('name')
    return render(request, 'recipes/recipe_search.html', {
        'results': results,
        'keyword': keyword,
        'filterform': filterform
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
            recipe.name = recipe.name.title()
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
        if request.method == 'POST':
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
def recipe_add_rate(request, recipe_pk):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        recipe_rate = RecipeRate.objects.filter(recipe=recipe, user=request.user).first()
        if recipe_rate is None:
            rate_form = recipeforms.RecipeRateForm(request.POST)
        else:
            rate_form = recipeforms.RecipeRateForm(request.POST, instance=recipe_rate)
        if rate_form.is_valid():
            recipe_rate = rate_form.save(commit=False)
            recipe_rate.recipe = recipe
            recipe_rate.user = request.user
            recipe_rate.save()
            messages.success(request, 'The recipe was rated successfully')
            print(recipe_rate.rate)
        return redirect('recipes:details', recipe_slug=recipe.slug)
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


@login_required(login_url="accounts:login")
def recipe_reply_comment(request, comment_pk):
    comment = get_object_or_404(RecipeComment, pk=comment_pk)
    if request.method == 'POST':
        comment_form = recipeforms.RecipeCommentForm(request.POST)
        if comment_form.is_valid():
            recipe_comment = comment_form.save(commit=False)
            recipe_comment.recipe = comment.recipe
            recipe_comment.user = request.user
            recipe_comment.parent = comment
            recipe_comment.save()
            messages.success(request, 'The comment was added successfully')
            return redirect('recipes:details', recipe_slug=comment.recipe.slug)
    else:
        comment_form = recipeforms.RecipeCommentForm
        return render(request, 'recipes/recipes_reply_to_comment.html',
                      {
                          'comment_form': comment_form,
                          'comment': comment
                      })
