
from .serializers import ProductSerializer, CartSerializer
from .models import Product, Cart
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from accounts.jwt_check import CookieJWTAuthentication



class ProductSearch(APIView):
    permission_classes=[]
    def get(self, request, search_name):
        try:

            if not search_name or not search_name.strip():
                return Response(
                    {'error': 'Search term cannot be empty!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            products = Product.objects.filter(
                Q(product_name__icontains=search_name) |
                Q(description__icontains=search_name)
            )

            if not products.exists():
                return Response({
                    'message': 'Products not found!',
                    'search_term': search_name,
                    'count':0,
                    'results': []
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSerializer(products, many=True)

            return Response({
                'search_term': search_name,
                'count': products.count(),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'An error occurred while searching products',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AllProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddToCart(APIView):
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        # Validate input data using CartSerializer with request in context
        serializer = CartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        # Get product (validation already ensures it exists)
        product = Product.objects.get(id=product_id)

        # Get or create cart item
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # If item already exists, update quantity
            cart_item.quantity += quantity
            cart_item.save()

        # Return response
        cart_serializer = CartSerializer(cart_item, context={'request': request})
        return Response(
            {
                'message': 'Item added to cart successfully',
                'cart_item': cart_serializer.data
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True, context={'request': request})
        return Response(
            {
                'message': 'Cart items retrieved successfully',
                'cart_items': serializer.data
            },
            status=status.HTTP_200_OK
        )


    
class UpdateProduct(APIView):
    def delete(self,request,pk):
        try:
            cart_product = Cart.objects.get(pk=pk)
            cart_product.delete()
            return Response(
                {'Cart Item Removed...'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Item Does not exist!'},
                status=status.HTTP_404_NOT_FOUND
            )
        



