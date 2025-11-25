from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import User

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None
        
        try:
            validated_token = self.get_validated_token(raw_token)
            
            # Extract user_id from the token payload
            user_id = validated_token.get('user_id')
            
            if user_id is None:
                raise AuthenticationFailed('Token contained no recognizable user identification')
            
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found', code='user_not_found')
            
            
            return user, validated_token
            
        except (InvalidToken, TokenError):
            raise AuthenticationFailed('Invalid or expired token')