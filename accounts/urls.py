from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profiles/<str:username>/', views.update_profile_view, name='view_profile'),
    path('profile/edit/', views.update_profile_view, name='edit_profile')
]
