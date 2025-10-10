from django.urls import path
from .views import UserRegistration, UserUpdates, UserLogin, UserProfile

urlpatterns = [
    path('api/auth/user-registration/',UserRegistration.as_view()),
    path('api/auth/user/<int:pk>/',UserUpdates.as_view()),
    path('api/auth/user-login/',UserLogin.as_view()),
    path('api/auth/user-profile/', UserProfile.as_view())
    
]
