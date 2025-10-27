from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .jwt_check import CookieJWTAuthentication


class UserRegistration(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"error": "username already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error":"email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {'message': 'User Created successfully..', 
                     'data': serializer.data},
                     status=status.HTTP_201_CREATED
                )
            
            except ValidationError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
    # def get(self,request):
    #     user = User.objects.all()
    #     serializer = UserSerializer(user, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserUpdates(APIView):
    permission_classes = []
    def get(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error': 'user Does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
            
    def put(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'User Does not exist!'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(
                {'message': 'User deleted Successfully!'},
                status=status.HTTP_204_NO_CONTENT
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User Does not exist!'},
                status=status.HTTP_404_NOT_FOUND
            )
        
class UserLogin(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': "Email and Password are Required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if user.password == password:
            refresh = RefreshToken.for_user(user)
            response = Response(
                {
                    'message': 'Login Successful',
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    'user': {
                        'email': user.email,
                        'username': user.username
                    }
                },
                status=status.HTTP_200_OK
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age = 10 * 24 * 60 * 60  # 10 days in seconds = 864,000
            )
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age = 7 * 24 * 60 * 60  # 7 days in seconds = 604,800
            )
            return response

        else:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserProfile(APIView):
    permission_classes = []
    authentication_classes = [CookieJWTAuthentication]  # Use custom authentication

    def get(self, request):
        try:
            # Check if user is authenticated
            if not request.user:
                return Response({
                    'error': 'Authentication required',
                    'message': 'Please login to access your profile'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            user = request.user  # Authenticated user from token
            
            # Build profile data
            profile_data = {
                'email': user.email,
                'username': user.username,
            }
            
            return Response({
                'message': f'Welcome Back {user.username}!',
                'user': profile_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Catch any other unexpected errors
            return Response({
                'error': 'An error occurred while retrieving profile',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


