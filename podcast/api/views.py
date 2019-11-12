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

    def get_serializer_class(self):
        if self.action == 'items':
            return RssItemSerializer
        else:
            return PodcastSerializer

    @action(detail=True)
    def items(self, request, pk=None):
        serializer_context = {
            'request': request,
        }
        podcast = Podcast.objects.get(id=pk)
        results = RssItem.objects.filter(creator=podcast).all()
        serializer = RssItemSerializer(results, context= serializer_context, many=True)
        return Response(serializer.data)

class RssItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rss feed items to be viewed or edited.
    """
    queryset = RssItem.objects.all()
    serializer_class = RssItemSerializer
