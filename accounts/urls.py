from django.urls import path
from .views import UserRegistration, UserUpdates, UserLogin, UserProfile, CheckAuthStatus

urlpatterns = [
    path('api/auth/user-registration/',UserRegistration.as_view()),
    path('api/auth/user/<int:pk>/',UserUpdates.as_view()),
    path('api/auth/user-login/',UserLogin.as_view()),
    path('api/auth/user-profile/', UserProfile.as_view()),
    path('api/check-auth/', CheckAuthStatus.as_view()),
    
]
