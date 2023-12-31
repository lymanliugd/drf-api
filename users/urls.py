"""App notes urls"""
from django.urls import path

from users import api_views

urlpatterns = [
    path(
        'auth/signup', 
        api_views.SignupApiView.as_view(),
        name='user-signup',
    ),
    path(
        'auth/login', 
        api_views.LoginApiView.as_view(),
        name='user-login',
    ),
]
