from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import ugettext_lazy as _
from .models import Recipe, RecipeType, RecipeSkill, RecipeComment, RecipeRate, RecipeIngredient, RecipeStep, \
    RecipeImage
from . import forms as recipeforms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from slugify import slugify
from datetime import datetime
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Avg, Q


# Create your views here.

def recipe_homepage(request):
    """
    View which is the homepage of the website. It shows the x latest recipes where x is
    MAX_LATEST_RECIPES in settings
    :param request:
    :return:
    """
    latest_recipes = Recipe.objects.filter(published=True).order_by('-published_at')[:settings.MAX_LATEST_RECIPES]
    return render(request, 'recipes/recipes_homepage.html', {
        'latest_recipes': latest_recipes,
    })


def recipe_details(request, recipe_slug):
    """
    View to display details page for a recipe
    :param request:
    :param recipe_slug: The slug of the recipe
    :return:
    """
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
                      'comment_form': comment_form,
                      'rate_form': rate_form,
                      'user': request.user
                  })


def recipe_search(request):
    """
    View to search a recipe based on a keyword (see handle_search method at the bottom of this file)
    :param request:
    :return:
    """
    return handle_search(request, Recipe.objects.filter(published=True), 'recipes/recipe_search.html', True)


def recipe_browse_all(request):
    """
    View to browse recipes globally
    :param request:
    :return:
    """
    return handle_search(request, Recipe.objects.filter(published=True),
                         'recipes/recipe_browse.html', False,
                         {'mode': 'all', })


def recipe_browse_category(request, category_slug):
    """
    View to browse recipes by categories (see handle_search method at the bottom of this file)
    :param request:
    :param category_slug: The name of the category
    :return:
    """
    category = get_object_or_404(RecipeType, slug=category_slug)
    return handle_search(request, Recipe.objects.filter(recipe_type=category, published=True),
                         'recipes/recipe_browse.html', False,
                         {'mode': 'category', 'category_slug': category_slug, 'category_name': category.name})


def recipe_browse_skill(request, skill_slug):
    """
    View to browse recipes by skill needed / difficulty (see handle_search method at the bottom of this file)
    :param request:
    :param skill_slug: The name of the skill
    :return:
    """
    skill = get_object_or_404(RecipeSkill, slug=skill_slug)
    return handle_search(request, Recipe.objects.filter(recipe_skill=skill, published=True),
                         'recipes/recipe_browse.html', False,
                         {'mode': 'skill', 'skill_slug': skill_slug, 'skill_name': skill.name})


@login_required(login_url="accounts:login")
def recipe_create(request):
    """
    View to create a recipe
    :param request:
    :return:
    """
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
            return handle_next(request, redirect('recipes:edit', recipe_slug=recipe.slug))
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
    """
    View to edit a recipe
    :param request:
    :param recipe_slug: The slug of the recipe
    :return:
    """
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
                return handle_next(request, redirect('recipes:edit', recipe_slug=recipe.slug))
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
    """
    View to delete a recipe based on his primary key
    :param request:
    :param recipe_pk: The primary key of the recipe
    :return:
    """
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    if recipe.author == request.user:
        recipe.delete()
        messages.success(request, _('The recipe was deleted successfully'))
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return handle_next(request, redirect('recipes:homepage'))


@login_required(login_url="accounts:login")
def recipe_add_image(request, recipe_pk):
    """
    View to add an additional image to a recipe. A limit exists for the number of images (see
    MAX_RECIPE_IMAGES in settings)
    :param request:
    :param recipe_pk: The primary key of the recipe
    :return:
    """
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if recipe.author == request.user:
            if recipe.images.count() < settings.MAX_RECIPE_IMAGES:
                image_form = recipeforms.RecipeImageForm(request.POST, request.FILES)
                if image_form.is_valid():
                    recipe_image = image_form.save(commit=False)
                    recipe_image.recipe = recipe
                    recipe_image.save()
                    recipe.updated_at = datetime.now()
                    recipe.save()
                    messages.success(request, _('The image was added successfully'))
                return handle_next(request, redirect('recipes:edit', recipe_slug=recipe.slug))
            else:
                messages.error(request, _("The maximum number of images by recipes has been exceeded"))
        else:
            messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:homepage')


@login_required(login_url="accounts:login")
def recipe_add_step(request, recipe_pk):
    """
    View to add a step. The order value is equal to the count step of the recipe + 1
    :param request:
    :param recipe_pk: Primary key of the recipe
    :return:
    """
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
            return handle_next(request, redirect('recipes:edit', recipe_slug=recipe.slug))
        else:
            messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:homepage')


@login_required(login_url="accounts:login")
def recipe_delete_step(request, step_pk):
    """
    View to delete a step. All steps after this one will have their order value decreased of 1
    :param request:
    :param step_pk:
    :return:
    """
    step = get_object_or_404(RecipeStep, pk=step_pk)
    if request.user == step.recipe.author:
        step.delete()
        next_steps = step.recipe.steps.filter(order__gte=step.order)
        for next_step in next_steps:
            next_step.order -= 1
            next_step.save()
        messages.success(request, _('The step was deleted successfully'))
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return handle_next(request, redirect('recipes:edit', recipe_slug=step.recipe.slug))


@login_required(login_url="accounts:login")
def recipe_up_step(request, step_pk):
    """
    View to increase the step order
    :param request:
    :param step_pk: Primary key of the RecipeStep
    :return:
    """
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
    return handle_next(request, redirect('recipes:edit', recipe_slug=step.recipe.slug))


@login_required(login_url="accounts:login")
def recipe_down_step(request, step_pk):
    """
    View to decrease the step order
    :param request:
    :param step_pk: Primary key of the RecipeStep
    :return:
    """
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
    return handle_next(request, redirect('recipes:edit', recipe_slug=step.recipe.slug))


@login_required(login_url="accounts:login")
def recipe_add_ingredient(request, recipe_pk):
    """
    View to add an ingredient to a Recipe
    :param request:
    :param recipe_pk: Primary key of the Recipe
    :return:
    """
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
            return handle_next(request, redirect('recipes:edit', recipe_slug=recipe.slug))
        else:
            messages.error(request, _("You're not the author of this recipe"))
    return redirect('recipes:homepage')


@login_required(login_url="accounts:login")
def recipe_add_rate(request, recipe_pk):
    """
    View to rate a Recipe (add or edit depending if it already exists)
    :param request:
    :param recipe_pk: The primary key of the recipe
    :return:
    """
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
            recipe_rate.updated_at = datetime.now()
            recipe_rate.save()
            messages.success(request, _('The recipe was rated successfully'))
        return handle_next(request, redirect('recipes:details', recipe_slug=recipe.slug))
    return redirect('recipes:homepage')


@login_required(login_url="accounts:login")
def recipe_add_comment(request, recipe_pk):
    """
    View to add a comment to a recipe
    :param request:
    :param recipe_pk: he primary key of the recipe
    :return:
    """
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        comment_form = recipeforms.RecipeCommentForm(request.POST)
        if comment_form.is_valid():
            recipe_comment = comment_form.save(commit=False)
            recipe_comment.recipe = recipe
            recipe_comment.user = request.user
            recipe_comment.save()
            messages.success(request, _('The comment was added successfully'))
        return handle_next(request, redirect('recipes:details', recipe_slug=recipe.slug))
    return redirect('recipes:homepage')


@login_required(login_url="accounts:login")
def recipe_reply_comment(request, comment_pk):
    """
    View to reply to a comment for a recipe
    :param request:
    :param comment_pk: Primary key of the comment
    :return:
    """
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
            return handle_next(request, redirect('recipes:details', recipe_slug=comment.recipe.slug))
    else:
        comment_form = recipeforms.RecipeCommentForm
        return render(request, 'recipes/recipes_reply_to_comment.html',
                      {
                          'comment_form': comment_form,
                          'comment': comment
                      })


@login_required(login_url="accounts:login")
def recipe_toogle_publish(request, recipe_pk):
    """
    View to publish / disable a recipe
    :param request:
    :param recipe_pk: The primary key of the recipe
    :return:
    """
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    if request.user == recipe.author:
        toogle = not recipe.published
        recipe.published = toogle
        if toogle:
            recipe.published_at = datetime.now()
            messages.success(request, _('The recipe was published'))
        else:
            messages.success(request, _('The recipe was unpublished'))
        recipe.save()
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return handle_next(request, redirect('recipes:edit', recipe_slug=recipe.slug))


@login_required(login_url="accounts:login")
def recipe_delete_image(request, image_pk):
    """
    View to delete an additional image for a recipe
    :param request:
    :param image_pk: The primary key of the Image
    :return:
    """
    image = get_object_or_404(RecipeImage, pk=image_pk)
    if request.user == image.recipe.author:
        image.delete()
        messages.success(request, _('The picture was deleted successfully'))
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return handle_next(request, redirect('recipes:edit', recipe_slug=image.recipe.slug))


@login_required(login_url="accounts:login")
def recipe_delete_ingredient(request, ingredient_pk):
    """
    View to delete an ingredient for a recipe
    :param request:
    :param ingredient_pk: The primary key of the ingredient
    :return:
    """
    ingredient = get_object_or_404(RecipeIngredient, pk=ingredient_pk)
    if request.user == ingredient.recipe.author:
        ingredient.delete()
        messages.success(request, _('The ingredient was deleted successfully'))
    else:
        messages.error(request, _("You're not the author of this recipe"))
    return handle_next(request, redirect('recipes:edit', recipe_slug=ingredient.recipe.slug))


# Handlers functions


def handle_search(request, base_recipes, template, require_keyword, other_args={}):
    """
    Utility method to handle the search feature for recipes on the website
    :param request:
    :param base_recipes: A base list of recipeswhich needs to be filtered / ordered
    :param template: The template which will handle all results at the end
    :param require_keyword: Do we Require keyword to filter the base_recipes ?
    :param other_args: Some other args passed to the template in case of
    :return:
    """
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if require_keyword and keyword == '':  # We require keyword but it is empty
            return redirect('recipes:homepage')
        recipes = base_recipes.filter(  # Search is based on contains in recipe name or ingredient name
            Q(name__contains=keyword) | Q(ingredients__ingredient__name__contains=keyword)).distinct()
    else:
        if require_keyword:  # There's no keyword and we require it
            return redirect('recipes:homepage')
        keyword = ''
        recipes = base_recipes
    return handle_filters(request, recipes, keyword, template, other_args)


def handle_filters(request, recipes, keyword, template, other_args={}):
    """
    Utility method to handle the filter / order feature for recipes on the website
    :param request:
    :param recipes: The list of recipes treated built by handle_search method
    :param keyword: The keyword found by handle_search method if there's one
    :param template: The template which will receive all results
    :param other_args: Some other args passed to the template in case of
    :return:
    """
    if 'filter' in request.GET and 'order' in request.GET:
        filt = request.GET['filter']  # A model field name
        order = request.GET['order']  # Can be '' for ASC or '-' for DESC
        if filt == 'recipe_rate':
            results = recipes.annotate(avg_rate=Avg('rates__rate')).order_by(order + 'avg_rate')
        else:
            results = recipes.order_by(order + filt)
    else:
        filt = 'name'
        order = ''
        results = recipes.order_by('name')  # By default, we order by name alphabetically
    filterform = recipeforms.RecipeFilterForm(keyword, filt, order)
    num_page = 1
    if 'num_page' in request.GET:  # For results pagination
        num_page = request.GET['num_page']
    paginator = Paginator(results, settings.MAX_SEARCH_RESULTS)
    args = {
        'results_paginator': paginator.page(num_page),
        'range_page': range(1, paginator.num_pages + 1),
        'number_results': results.count,
        'keyword': keyword,
        'filter': filt,
        'order': order,
        'filterform': filterform
    }
    return render(request, template, {**args, **other_args})


def handle_next(request, default_redirect):
    """
    Utility method to handle next parameter to force specific redirect
    :param request: The request where we search for next parameter
    :param default_redirect: The default redirect if next is not found
    :return:
    """
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    else:
        return default_redirect
