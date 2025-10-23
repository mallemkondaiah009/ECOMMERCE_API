from rest_framework.serializers import ModelSerializer
from .models import Category, Product

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields= '__all__'

