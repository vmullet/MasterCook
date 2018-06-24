from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CookerAuthenticationForm, CookerCreationForm, CookerProfileForm, UserEditForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here


def signup_view(request):
    if request.method == 'POST':
        form = CookerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request, user)
            return redirect('recipes:list')
    else:
        form = CookerCreationForm()
    return render(request, 'accounts/accounts_signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CookerAuthenticationForm(data=request.POST)
        if form.is_valid():
            # log in the user in
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('recipes:list')
    else:
        form = CookerAuthenticationForm()
    return render(request, 'accounts/accounts_login.html', {'form': form})


def logout_view(request):
        logout(request)
        return redirect('recipes:list')


def profile_view(request,username):
    user = get_object_or_404(User, username=username)
    return render(request, 'accounts/accounts_profile_view.html', {'user': user})


@login_required(login_url='accounts:login')
def update_profile_view(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = CookerProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile saved')
        else:
            messages.error(request, 'Please correct the error')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = CookerProfileForm(instance=request.user.profile)
    return render(request, 'accounts/accounts_profile_edit.html',
                  {'user': request.user,
                   'user_form': user_form,
                   'profile_form': profile_form
                   })
