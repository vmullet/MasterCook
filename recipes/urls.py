from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_homepage, name='homepage'),
    path('recipes/list', views.recipe_list, name='list'),
    path('recipes/details/<slug:recipe_slug>', views.recipe_details, name='details'),
    path('recipes/create', views.recipe_create, name='create'),
    path('recipes/edit/<slug:recipe_slug>', views.recipe_edit, name='edit'),
    path('recipes/delete/<int:recipe_pk>', views.recipe_delete, name='delete')
]
