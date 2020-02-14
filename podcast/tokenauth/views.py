from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from . import settings as ta_settings
from .helpers import email_login_link
from podcast.users.models import ClubUser
import json

@api_view(['POST'])
@parser_classes([JSONParser])
def email_post(request, format=None):
    """
    Process the submission of the form with the user's 
    email and mail them a link.
    """
    if request.user.is_authenticated:
        return Response({'Error': "You are already logged in."}, 
            status=status.HTTP_202_ACCEPTED)

    email = ta_settings.NORMALIZE_EMAIL(request.data['email'])
    if not email:
        return Response({'Error': "Please provide email"}, 
            status=status.HTTP_400_BAD_REQUEST)

    email_login_link(request, email)
    
    return Response({'Info': 'Login email sent! Please check ' +
        'your inbox and click on the link to be logged in.'}, 
        status=status.HTTP_200_OK)

@api_view(['POST'])
@parser_classes([JSONParser])
def token_post(request, token=None):
    """Validate the token the user submitted."""
    user = authenticate(request, token=token)
    if user is None:
        return Response({'Error': "The login link is invalid or has expired, \
            or you are not allowed to log in, please try again."}, 
            status=status.HTTP_400_BAD_REQUEST)

    if request.user.is_authenticated:
        return Response({'Error': "You are already logged in."}, 
            status=status.HTTP_202_ACCEPTED)

    djlogin(request, user)
    return Response(
        json.dumps(user.email), 
        status=status.HTTP_200_OK, 
        content_type="application/json")

@login_required
def logout(request):
    djlogout(request)
    return Response({'Info': 'You are logged out.'}, 
        status=status.HTTP_200_OK)