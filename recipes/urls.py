from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_homepage, name='homepage'),
    path('create', views.recipe_create, name='create'),
    path('<slug:recipe_slug>/edit', views.recipe_edit, name='edit'),
    path('delete/<int:recipe_pk>', views.recipe_delete, name='delete'),
    path('<int:recipe_pk>/comment/add', views.recipe_add_comment, name='add_comment'),
    path('<int:recipe_pk>/image/add', views.recipe_add_image, name='add_image'),
    path('<int:recipe_pk>/step/add', views.recipe_add_step, name='add_step'),
    path('<int:recipe_pk>/ingredient/add', views.recipe_add_ingredient, name='add_ingredient'),
    path('<int:recipe_pk>/rate/add', views.recipe_add_rate, name='add_rate'),
    path('<slug:recipe_slug>/details', views.recipe_details, name='details'),
    path('comment/<int:comment_pk>/replyto', views.recipe_reply_comment, name='reply_to_comment'),
    path('search', views.recipe_search, name='search'),
    path('browse/category/<str:category_name>', views.recipe_browse_category, name='browse_category'),
    path('browse/skill/<str:skill_name>', views.recipe_browse_skill, name='browse_skill')
]
