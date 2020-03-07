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
from podcast.users.models import ClubUser
import json

@login_required
def add_item_to_playing_list(request):
    if not request.user:
        return Response({'Error': "User does not exist."}, 
            status=status.HTTP_400_BAD_REQUEST)
    

