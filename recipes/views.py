from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from .models import Recipe, RecipeType, RecipeSkill, RecipeComment, RecipeRate, RecipeIngredient, RecipeStep, \
    RecipeImage
from . import forms as recipeforms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from slugify import slugify
from datetime import datetime
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Avg, Q


# Create your views here.

def recipe_homepage(request):
    latest_recipes = Recipe.objects.filter(published=True).order_by('-published_at')[:settings.MAX_LATEST_RECIPES]
    return render(request, 'recipes/recipes_homepage.html', {
        'latest_recipes': latest_recipes,
    })


def recipe_details(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug, published=True)
    comments = recipe.comments.order_by('-created_at').all()
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
                      'comment_paginator': paginator.page(num_page),
                      'range_page': range(1, paginator.num_pages + 1),
                      'number_comments': comments.count,
                      'comment_form': comment_form,
                      'rate_form': rate_form,
                      'user': request.user
                  })


def recipe_search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        recipes = Recipe.objects.filter(published=True)
        recipes = recipes.filter(
            Q(name__contains=keyword) | Q(ingredients__ingredient__name__contains=keyword)).distinct()
        if 'filter' in request.GET and 'order' in request.GET:
            filt = request.GET['filter']
            order = request.GET['order']
            if filt == 'recipe_rate':
                results = recipes.annotate(avg_rate=Avg('rates__rate')).order_by(order + 'avg_rate')
            else:
                results = recipes.order_by(order + filt)
        else:
            filt = 'name'
            order = ''
            results = recipes.order_by('name')
        filterform = recipeforms.RecipeFilterForm(keyword, filt, order)
        num_page = 1
        if 'num_page' in request.GET:
            num_page = request.GET['num_page']
        paginator = Paginator(results, settings.MAX_SEARCH_RESULTS)
        return render(request, 'recipes/recipe_search.html', {
            'results_paginator': paginator.page(num_page),
            'current_page': num_page,
            'range_page': range(1, paginator.num_pages + 1),
            'number_results': results.count,
            'keyword': keyword,
            'filter': filt,
            'order': order,
            'filterform': filterform
        })
    return redirect('recipes:list')


def recipe_browse_category(request, category_name):
    category = get_object_or_404(RecipeType, name=category_name)
    recipes = Recipe.objects.filter(recipe_type=category, published=True)
    keyword = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        recipes = recipes.filter(
            Q(name__contains=keyword) | Q(ingredients__ingredient__name__contains=keyword)).distinct()
    if 'filter' in request.GET and 'order' in request.GET:
        filt = request.GET['filter']
        order = request.GET['order']
        if filt == 'recipe_rate':
            results = recipes.annotate(avg_rate=Avg('rates__rate')).order_by(order + 'avg_rate')
        else:
            results = recipes.order_by(order + filt)
    else:
        filt = 'name'
        order = ''
        results = recipes.order_by('name')
    filterform = recipeforms.RecipeFilterForm(keyword, filt, order)
    num_page = 1
    if 'num_page' in request.GET:
        num_page = request.GET['num_page']
    paginator = Paginator(results, settings.MAX_SEARCH_RESULTS)
    return render(request, 'recipes/recipe_browse.html', {
        'mode': 'category',
        'category_name': category_name,
        'results_paginator': paginator.page(num_page),
        'range_page': range(1, paginator.num_pages + 1),
        'number_results': results.count,
        'keyword': keyword,
        'filter': filt,
        'order': order,
        'filterform': filterform
    })


def recipe_browse_skill(request, skill_name):
    skill = get_object_or_404(RecipeSkill, name=skill_name)
    recipes = Recipe.objects.filter(recipe_skill=skill, published=True)
    keyword = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        recipes = recipes.filter(
            Q(name__contains=keyword) | Q(ingredients__ingredient__name__contains=keyword)).distinct()
    if 'filter' in request.GET and 'order' in request.GET:
        filt = request.GET['filter']
        order = request.GET['order']
        if filt == 'recipe_rate':
            results = recipes.annotate(avg_rate=Avg('rates__rate')).order_by(order + 'avg_rate')
        else:
            results = recipes.order_by(order + filt)
    else:
        filt = 'name'
        order = ''
        results = recipes.order_by('name')
    filterform = recipeforms.RecipeFilterForm(keyword, filt, order)
    num_page = 1
    if 'num_page' in request.GET:
        num_page = request.GET['num_page']
    paginator = Paginator(results, settings.MAX_SEARCH_RESULTS)
    return render(request, 'recipes/recipe_browse.html', {
        'mode': 'skill',
        'skill_name': skill_name,
        'results_paginator': paginator.page(num_page),
        'range_page': range(1, paginator.num_pages + 1),
        'number_results': results.count,
        'keyword': keyword,
        'filter': filt,
        'order': order,
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
                messages.success(request, _("Recipe updated successfully"))
                return redirect('recipes:edit', recipe_slug=recipe.slug)
        else:
            edit_form = recipeforms.RecipeEditForm(instance=recipe)
            cost_form = recipeforms.RecipeCostForm(instance=recipe.recipe_cost)
    else:
        messages.error(request, _("You're not the author of this recipe"))
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
            messages.success(request, _('The recipe was deleted successfully'))
        else:
            messages.error(request, _("You're not the author of this recipe"))
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
                messages.success(request, _('The image was added successfully'))
            return redirect('recipes:edit', recipe_slug=recipe.slug)
        else:
            messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:homepage')


@login_required(login_url="accounts:login")
def recipe_add_step(request, recipe_pk):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if recipe.author == request.user:
            step_form = recipeforms.RecipeStepForm(request.POST)
            if step_form.is_valid():
                recipe_step = step_form.save(commit=False)
                recipe_step.order = recipe.steps.count() + 1
                recipe_step.recipe = recipe
                recipe_step.save()
                recipe.updated_at = datetime.now()
                recipe.save()
                messages.success(request, _('The step was added successfully'))
            return redirect('recipes:edit', recipe_slug=recipe.slug)
        else:
            messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:homepage')


@login_required(login_url="accounts:login")
def recipe_delete_step(request, step_pk):
    step = get_object_or_404(RecipeStep, pk=step_pk)
    if request.user == step.recipe.author:
        step.delete()
        messages.success(request, _('The step was deleted successfully'))
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:edit', recipe_slug=step.recipe.slug)


@login_required(login_url="accounts:login")
def recipe_up_step(request, step_pk):
    step = get_object_or_404(RecipeStep, pk=step_pk)
    if request.user == step.recipe.author:
        if step.order > 1:
            step.order -= 1
            step.save()
            previous_step = step.recipe.steps.filter(order=step.order).exclude(pk=step_pk).first()
            previous_step.order += 1
            previous_step.save()
            messages.success(request, _('The step was updated successfully'))
        else:
            messages.warning(request, _('The step is already the first one'))
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:edit', recipe_slug=step.recipe.slug)


@login_required(login_url="accounts:login")
def recipe_down_step(request, step_pk):
    step = get_object_or_404(RecipeStep, pk=step_pk)
    steps = step.recipe.steps
    if request.user == step.recipe.author:
        if step.order < steps.count():
            step.order += 1
            step.save()
            next_step = steps.filter(order=step.order).exclude(pk=step_pk).first()
            next_step.order -= 1
            next_step.save()
            messages.success(request, _('The step was updated successfully'))
        else:
            messages.warning(request, _('The step is already the last one'))
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:edit', recipe_slug=step.recipe.slug)


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
                messages.success(request, _('The ingredient was added successfully'))
            return redirect('recipes:edit', recipe_slug=recipe.slug)
        else:
            messages.error(request, _("You're not the author of this recipe"))
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
            messages.success(request, _('The recipe was rated successfully'))
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
            messages.success(request, _('The comment was added successfully'))
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


@login_required(login_url="accounts:login")
def recipe_toogle_publish(request, recipe_pk):
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    if request.user == recipe.author:
        toogle = not recipe.published
        recipe.published = toogle
        recipe.save()
        if toogle:
            messages.success(request, _('The recipe was published'))
        else:
            messages.success(request, _('The recipe was unpublished'))
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:edit', recipe_slug=recipe.slug)


@login_required(login_url="accounts:login")
def recipe_delete_image(request, image_pk):
    image = get_object_or_404(RecipeImage, pk=image_pk)
    if request.user == image.recipe.author:
        image.delete()
        messages.success(request, _('The picture was deleted successfully'))
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:edit', recipe_slug=image.recipe.slug)





@login_required(login_url="accounts:login")
def recipe_delete_ingredient(request, ingredient_pk):
    ingredient = get_object_or_404(RecipeIngredient, pk=ingredient_pk)
    if request.user == ingredient.recipe.author:
        ingredient.delete()
        messages.success(request, _('The ingredient was deleted successfully'))
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:edit', recipe_slug=ingredient.recipe.slug)
