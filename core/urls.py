from django.urls import path, include
from django.views import *
from core.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('logout', logout, name='logout'),
    path('register/', register, name='register'),
    path('header/', header, name='header'),
    path('logout/', auth_views.LogoutView.as_view, name='logout'),
]

