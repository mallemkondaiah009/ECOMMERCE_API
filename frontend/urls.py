from django.urls import path
from .views import register_view, login_view, profile_view

urlpatterns = [
    path('register/', register_view, name='register_view'),
    path('login/', login_view, name='login_view'),
    path('profile/', profile_view, name='profile_view')
]
