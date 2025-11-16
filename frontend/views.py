from django.shortcuts import render

def register_view(request):
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')

def profile_view(request):
    return render(request, 'profile.html')

def home_view(request):
    return render(request, 'home.html')

def cart_view(request):
    return render(request, 'cart.html')

def productView_view(request):
    return render(request, 'view_product.html')

