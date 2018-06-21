from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_list),
    path('recipes/<int:id>', views.recipe_details)
]
