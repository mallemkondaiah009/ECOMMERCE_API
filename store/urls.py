
from django.urls import path
from .views import ProductSearch, AllProducts, AddToCart, UpdateProduct


urlpatterns = [
    path('api/search/<str:search_name>/',ProductSearch.as_view()),
    path('api/products/', AllProducts.as_view()),
    path('api/add-to-cart/', AddToCart.as_view()),
    path('api/cart-item-remove/<int:pk>/', UpdateProduct.as_view()),
]