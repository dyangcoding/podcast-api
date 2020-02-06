from rest_framework import status, exceptions
from django.contrib.auth import get_user_model
from podcast.users.models import ClubUser
from . import settings as ta_settings
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from podcast.settings.base import get_env_variable
import jwt

class JWTTokenBackend:
    def get_user(self, user_id):
        """Get a user by their primary key."""
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, token=None):
        """Authenticate a user given a signed token."""
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token=="null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(request, token)
    
    def authenticate_credentials(self, request, token):
        secret = get_env_variable('SECRET_KEY')
        msg = {'Error': "Token mismatch",'status' :"401"}
        try:
            payload = jwt.decode(token, secret, algorithms=[ta_settings.JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return Response({'Error': "Token is invalid"}, status="403")
        
        user = ClubUser.objects.get(id=payload['user_id'])
        #reset user to active
        user.is_active = True
        user.save()

        request.user = user

        return user
