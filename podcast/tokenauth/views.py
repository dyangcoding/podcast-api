from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

@api_view(['POST'])
@parser_classes([JSONParser])
def email_post(request, format=None):
    """Process the submission of the form with the user's 
        email and mail them a link.
    """
    email = request.data['email']
    print('submitted email'.format(email))
    return Response({'received data': request.data})

@api_view(['POST'])
@parser_classes([JSONParser])
def token_post(request, token):
    pass

@login_required
def logout(request):
    pass