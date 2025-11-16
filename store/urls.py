
from django.urls import path
from .views import ProductSearch, AllProducts, AddToCart, DisplayProductWithId, RandomProducts


urlpatterns = [
    path('api/search/<str:search_name>/',ProductSearch.as_view()),
    path('api/products/', AllProducts.as_view()),
    path('api/add-to-cart/', AddToCart.as_view()),
    path('api/product/<int:pk>/', DisplayProductWithId.as_view()),
    path('api/random-products/',RandomProducts.as_view() )
]