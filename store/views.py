
from .serializers import ProductSerializer
from .models import Product,Category
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError


class ProductSearch(APIView):
    permission_classes=[]
    def get(self, request,search_name):
        products = Product.objects.filter(
            Q(product_name__icontains=search_name) |
            Q(description__icontains=search_name)
        )

        serializer = ProductSerializer(products, many=True)

        return Response({
            'search_term': search_name,
            'count': products.count(),
            'results': serializer.data
        },
        status=status.HTTP_200_OK)