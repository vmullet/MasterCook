from django.shortcuts import redirect
from django.utils import translation

# Create your views here.


def switch_lang_view(request, user_language):
    """
    View to switch language
    :param request:
    :param user_language: The user_language code (fr for France, en for English etc...)
    :return:
    """
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    if 'next' in request.GET:
        return redirect(request.GET.get('next'))
    else:
        return redirect('recipes:list')
