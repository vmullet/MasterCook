from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_homepage, name='homepage'),
    path('recipes/list', views.recipe_list, name='list'),
    path('recipes/create', views.recipe_create, name='create'),
    path('recipes/<slug:recipe_slug>/edit', views.recipe_edit, name='edit'),
    path('recipes/delete/<int:recipe_pk>', views.recipe_delete, name='delete'),
    path('recipes/<int:recipe_pk>/comment/add', views.recipe_add_comment, name='add_comment'),
    path('recipes/<int:recipe_pk>/image/add', views.recipe_add_image, name='add_image'),
    path('recipes/<int:recipe_pk>/step/add', views.recipe_add_step, name='add_step'),
    path('recipes/<int:recipe_pk>/ingredient/add', views.recipe_add_step, name='add_ingredient'),
    path('recipes/<slug:recipe_slug>/details', views.recipe_details, name='details'),
]
