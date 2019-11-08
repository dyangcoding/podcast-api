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

class PodcastViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows podcasts to be viewed or edited.
    """
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    lookup_field = 'name'

    @action(detail=True)
    def rss_items(self, request, name=None):
        podcast = Podcast.objects.get(name=name)
        items = RssItem.objects.filter(creator=podcast).all()
        return Response(items)

class RssItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rss feed items to be viewed or edited.
    """
    queryset = RssItem.objects.all()
    serializer_class = RssItemSerializer
