from django.urls import path
from . import views

# Create your urls here.
urlpatterns = [
    path('', views.index, name = 'index'),
    path('index', views.index, name = 'index'),
    path('accounts/login', views.Authentication.as_view(), name = 'login'),
    path('accounts/signup', views.Authentication.as_view(), name = 'signup'),
    path('accounts/logout', views.Exit.as_view(), name = 'logout'),
    path('users/profile', views.PersonalInfo.as_view(), name = 'profile'),
]