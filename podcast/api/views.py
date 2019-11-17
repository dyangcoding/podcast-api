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
        podcast = Podcast.objects.get(id=pk)
        results = RssItem.objects \
                    .filter(creator=podcast) \
                    .all() \
                    .order_by('-pub_date')
        page = self.paginate_queryset(results)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

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
