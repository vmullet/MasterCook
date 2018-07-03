from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CookerAuthenticationForm, CookerCreationForm, CookerProfileForm, UserEditForm, \
    CookerChangePasswordForm
from .models import CookerProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your views here


def signup_view(request):
    """
    View to allow a user to sign up on the website
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = CookerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile = CookerProfile.objects.create(user=user)
            # log the user in
            login(request, user)
            return redirect('recipes:homepage')
    else:
        form = CookerCreationForm()
    return render(request, 'accounts/accounts_signup.html', {'form': form})


def login_view(request):
    """
    View to allow a user to login on the website
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = CookerAuthenticationForm(data=request.POST)
        if form.is_valid():
            # log in the user in
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('recipes:homepage')
    else:
        form = CookerAuthenticationForm()
    return render(request, 'accounts/accounts_login.html', {'form': form})


def logout_view(request):
    """
    View to allow a user to logout
    :param request:
    :return:
    """
    logout(request)
    return redirect('recipes:homepage')


def profile_view(request, username):
    """
    View to consult a user profile
    :param request:
    :param username: The username of the user with this profile
    :return:
    """
    user = get_object_or_404(User, username=username)
    if hasattr(user, 'profile') is False:
        user.profile = CookerProfile.objects.create(user=user)
        user.save()
    return render(request, 'accounts/accounts_profile_view.html', {'user': user})


@login_required(login_url='accounts:login')
def update_profile_view(request):
    """
    View to update profile informations for the current user
    :param request:
    :return:
    """
    if hasattr(request.user, 'profile') is False:
        request.user.profile = CookerProfile.objects.create(user=request.user)
        request.user.save()
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = CookerProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Profile saved successfully'))
        else:
            messages.error(request, _('Please correct the error'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = CookerProfileForm(instance=request.user.profile)
    return render(request, 'accounts/accounts_profile_edit.html',
                  {'user': request.user,
                   'user_form': user_form,
                   'profile_form': profile_form
                   })


@login_required(login_url='accounts:login')
def update_password_view(request):
    """
    View to update the password of the current user
    :param request:
    :return:
    """
    if request.method == 'POST':
        password_form = CookerChangePasswordForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('accounts:edit_password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        password_form = CookerChangePasswordForm(request.user)
    return render(request, 'accounts/accounts_password_edit.html', {
        'form': password_form
    })


@login_required(login_url='accounts:login')
def user_dashboard_view(request):
    """
    View to consult the dashboard of the current user
    :param request:
    :return:
    """
    recipes = request.user.recipes.all()
    rates = request.user.rates.all()
    return render(request, 'accounts/accounts_user_dashboard.html', {
        'recipes': recipes,
        'rates': rates,
    })
