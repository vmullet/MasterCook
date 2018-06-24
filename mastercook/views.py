from django.shortcuts import render


def shortcodes(request):
    return render(request, 'shortcodes.html')

