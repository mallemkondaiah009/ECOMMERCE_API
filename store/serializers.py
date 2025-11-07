from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product, Cart
from accounts.serializers import UserSerializer


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields= '__all__'

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  #It Display full product details on response

    class Meta:
        model = Cart
        fields = '__all__'
        


        

