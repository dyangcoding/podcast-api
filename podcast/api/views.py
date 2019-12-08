from django.contrib.auth.models import User
from rest_framework import viewsets, status
from podcast.api.serializers import UserSerializer, RssItemSerializer, PodcastSerializer
from .models import RssItem, Podcast
from django.utils import timezone
from django.db.models import Q
from operator import or_
from functools import reduce
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class PodcastViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows podcasts to be viewed.
    """
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

class RssItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rss feed items to be viewed.
    """
    cat_queryKey_mapper = {
        'IT': 1,
        'Entrepreneurship': 2,
        'Finance': 3
    }

    date_querykey_mapper = {
        'Last24': 1,
        'PastWeek': 7,
        'PastMonth': 30,
        'PastYear': 365
    }

    serializer_class = RssItemSerializer
    def get_queryset(self):
        """    
        Optionally restricts the returned items to a given category,
        by filtering against a `category` query parameter in the URL.
        """
        queryset = RssItem.objects.all().order_by('-pub_date')
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryKey = self.cat_queryKey_mapper[category]
            queryset = queryset.filter(creator__category=queryKey)

        query_date = self.request.query_params.get('date', None)
        if query_date is not None:
            day_from_now = self.date_querykey_mapper[query_date]
            time = timezone.now() - timezone.timedelta(days=day_from_now)
            queryset = queryset.filter(pub_date__gte=time)

        search_key = self.request.query_params.get('search', None)
        if search_key is not None:
            q_list = [Q(title__icontains=search_key), 
                        Q(description__icontains=search_key),
                        Q(creator__name__icontains=search_key),
                        Q(creator__base_url__icontains=search_key)]
            filter_key = reduce(or_, q_list)
            queryset = queryset.filter(filter_key) 

        return queryset
    
    @action(detail=True, methods=['post'])
    def upVote(self, request, pk=None):
        item = self.get_object()
        serializer = RssItemSerializer(data=request.data)
        if serializer.is_valid():
            item.set_likes(serializer.data['likes'])
            return Response({'status': 'updated item likes count'})
        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
