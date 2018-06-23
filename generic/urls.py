from django.urls import path
from . import views

app_name = 'generic'

urlpatterns = [
    path('changueLocale/<str:user_language>', views.switch_lang_view, name='switch_language'),
]
