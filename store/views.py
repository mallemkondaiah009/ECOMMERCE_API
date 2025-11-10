
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
        try:
            # Get and validate product_id
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)
            action = request.data.get('action', 'add')  # 'add', 'set', or 'decrease'
            
            # Validate product_id exists
            if not product_id:
                return Response(
                    {'error': 'Product ID is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate quantity
            if not isinstance(quantity, int) or quantity < 1:
                return Response(
                    {'error': 'Quantity must be a positive integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate action
            if action not in ['add', 'set', 'decrease']:
                return Response(
                    {'error': 'Action must be "add", "set", or "decrease"'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate product exists
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {'error': 'Product not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get or create cart item
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                # Handle different actions
                if action == 'add':
                    cart_item.quantity += quantity
                elif action == 'decrease':
                    cart_item.quantity -= quantity
                    # If quantity becomes 0 or less, delete the item
                    if cart_item.quantity <= 0:
                        cart_item.delete()
                        return Response(
                            {'message': 'Item removed from cart'},
                            status=status.HTTP_200_OK
                        )
                # elif action == 'set':
                #     cart_item.quantity = quantity
                
                cart_item.save()

            # Return response
            cart_serializer = CartSerializer(cart_item)
            return Response(
                {
                    'message': 'Cart updated successfully',
                    'cart_item': cart_serializer.data
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        
        except ValueError as e:
            return Response(
                {'error': f'Invalid data format: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            # Log the error for debugging
            # logger.error(f"Error adding item to cart: {str(e)}")
            return Response(
                {'error': 'An unexpected error occurred while updating cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
        



