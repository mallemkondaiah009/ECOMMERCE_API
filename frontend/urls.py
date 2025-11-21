from django.urls import path
from .views import register_view, login_view, profile_view, home_view, cart_view, productView_view

urlpatterns = [
    path('', home_view, name='home_view'),
    path('register/', register_view, name='register_view'),
    path('login/', login_view, name='login_view'),
    path('profile/', profile_view, name='profile_view'),
    path('cart/', cart_view ),
    path('product/checkout/', productView_view)
    
]
