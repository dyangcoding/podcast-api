from rest_framework import status, exceptions
from django.contrib.auth import get_user_model
from podcast.users.models import ClubUser
from . import settings as ta_settings
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from podcast.settings.base import get_env_variable
import jwt, json

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

        return self.authenticate_credentials(token)
    
    def authenticate_credentials(self, token):
        secret = get_env_variable('SECRET_KEY')
        payload = jwt.decode(token, secret)
        userid = payload['id']
        msg = {'Error': "Token mismatch",'status' :"401"}
        try:
            user = ClubUser.objects.get(id=userid)
            if not user.token['token'] == token:
                raise exceptions.AuthenticationFailed(msg)
            #reset user to active
            user.is_active = True
            user.save()
               
        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return Response({'Error': "Token is invalid"}, status="403")
        except User.DoesNotExist:
            return Response({'Error': "Internal server error"}, status="500") 

        return (user, token)
