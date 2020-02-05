from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout

from . import settings as ta_settings
from .helpers import email_login_link

from podcast.users.models import ClubUser

@api_view(['POST'])
@parser_classes([JSONParser])
def email_post(request, format=None):
    """
    Process the submission of the form with the user's 
    email and mail them a link.
    """
    if request.user.is_authenticated:
        pass

    email = ta_settings.NORMALIZE_EMAIL(request.data['email'])
    if not email:
        return Response({'Error': "Please provide email"}, status="400")

    email_login_link(request, email)
    
    return Response({'received data': request.data})

@api_view(['POST'])
@parser_classes([JSONParser])
def token_post(request, token):
    """Validate the token the user submitted."""
    user = authenticate(request, token=token)
    if user is None:
        pass

    if request.user.is_authenticated:
        pass

    djlogin(request, user)

@login_required
def logout(request):
    djlogout(request)
    pass