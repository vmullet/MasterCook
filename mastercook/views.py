from django.shortcuts import render, redirect


def shortcodes(request):
    return render(request, 'shortcodes.html')


def root_redirect(request):
    return redirect('recipes:homepage')
