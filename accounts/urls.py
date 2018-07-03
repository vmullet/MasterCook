from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profiles/<str:username>/', views.profile_view, name='view_profile'),
    path('profile/edit/', views.update_profile_view, name='edit_profile'),
    path('password/edit/', views.update_password_view, name='edit_password'),
    path('mydashboard/', views.user_dashboard_view, name='my_dashboard'),
]
