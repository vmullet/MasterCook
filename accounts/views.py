from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CookerAuthenticationForm

# Create your views here


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request, user)
            return redirect('recipes:list')
    else:
        form = UserCreationForm()
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


