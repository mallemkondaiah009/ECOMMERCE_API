# payments/urls.py
from django.urls import path
from .views import CreateOrderAPIView, VerifyPaymentAPIView

urlpatterns = [
    path('api/create-order/', CreateOrderAPIView.as_view(), name='create_order'),
    path('api/verify-payment/', VerifyPaymentAPIView.as_view(), name='verify_payment'),
]