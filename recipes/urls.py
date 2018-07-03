from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_homepage, name='homepage'),
    path('create', views.recipe_create, name='create'),
    path('delete/<int:recipe_pk>', views.recipe_delete, name='delete'),
    path('<slug:recipe_slug>/edit', views.recipe_edit, name='edit'),
    path('<int:recipe_pk>/publish_toogle', views.recipe_toogle_publish, name='publish_toogle'),
    path('<int:recipe_pk>/comment/add', views.recipe_add_comment, name='add_comment'),
    path('<int:recipe_pk>/image/add', views.recipe_add_image, name='add_image'),
    path('image/delete/<int:image_pk>', views.recipe_delete_image, name='delete_image'),
    path('<int:recipe_pk>/step/add', views.recipe_add_step, name='add_step'),
    path('step/up/<int:step_pk>', views.recipe_up_step, name='up_step'),
    path('step/down/<int:step_pk>', views.recipe_down_step, name='down_step'),
    path('step/delete/<int:step_pk>', views.recipe_delete_step, name='delete_step'),
    path('<int:recipe_pk>/ingredient/add', views.recipe_add_ingredient, name='add_ingredient'),
    path('ingredient/delete/<int:ingredient_pk>', views.recipe_delete_ingredient, name='delete_ingredient'),
    path('<int:recipe_pk>/rate/add', views.recipe_add_rate, name='add_rate'),
    path('<slug:recipe_slug>/details', views.recipe_details, name='details'),
    path('comment/<int:comment_pk>/replyto', views.recipe_reply_comment, name='reply_to_comment'),
    path('search', views.recipe_search, name='search'),
    path('browse/all', views.recipe_browse_all, name='browse_all'),
    path('browse/category/<slug:category_slug>', views.recipe_browse_category, name='browse_category'),
    path('browse/skill/<slug:skill_slug>', views.recipe_browse_skill, name='browse_skill')
]
