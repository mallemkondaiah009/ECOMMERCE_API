from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product, Cart


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields= '__all__'

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(min_value=1, default=1)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['id', 'added_at', 'updated_at']

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")
        return value


        

