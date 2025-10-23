
from django.urls import path
from .views import ProductSearch


urlpatterns = [
    path('api/search/<str:search_name>/',ProductSearch.as_view()),
    
]