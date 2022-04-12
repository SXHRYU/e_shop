from django.urls import path
from .views import (
    auth_login_view, 
    auth_logout_view,
    )


urlpatterns = [
    path('login/', auth_login_view, name='auth-login'),
    path('logout/', auth_logout_view, name='auth-logout'),
]   