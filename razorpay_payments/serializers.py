# payments/serializers.py
from rest_framework import serializers
from .models import RazorpayPayment
from store.serializers import ProductSerializer

class PaymentSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  #It Display full product details on response

    class Meta:
        model = RazorpayPayment
        fields = '__all__'