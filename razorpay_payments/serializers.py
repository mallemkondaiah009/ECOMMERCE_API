# payments/serializers.py
from rest_framework import serializers
from .models import RazorpayPayment

class PaymentSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_id   = serializers.IntegerField(write_only=True)   # we receive product_id from frontend

    class Meta:
        model = RazorpayPayment
        fields = '__all__'
        read_only_fields = ['order_id', 'payment_id', 'signature', 'status', 'created_at', 'user']