from django.contrib.auth.models import User
from rest_framework import viewsets
from podcast.api.serializers import UserSerializer, RssItemSerializer, PodcastSerializer
from .models import RssItem, Podcast
from rest_framework.response import Response
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class PodcastViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows podcasts to be viewed or edited.
    """
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

class RssItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rss feed items to be viewed or edited.
    """
    serializer_class = RssItemSerializer
    def get_queryset(self):
        """    
        Optionally restricts the returned items to a given category,
        by filtering against a `category` query parameter in the URL.
        """
        queryset = RssItem.objects.all().order_by('-pub_date')
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(creator__category=category)
        return queryset
