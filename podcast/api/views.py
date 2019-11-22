from django.contrib.auth.models import User
from rest_framework import viewsets
from podcast.api.serializers import UserSerializer, RssItemSerializer, PodcastSerializer
from .models import RssItem, Podcast
from datetime import date

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
    cat_queryKey_mapper = {
        'IT': 1,
        'Entrepreneurship': 2,
        'Finance': 3
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
            today = date.today()
            if date == 'Last 24':
                queryset = queryset.filter(pub_date__day=today.day)
            elif date == 'Past Week':
                queryset = queryset.filter(pub_date__week=today.week)
            elif date == 'Past Month':
                queryset = queryset.filter(pub_date__month=today.month)
            else:
                queryset = queryset.filter(pub_date__year=today.year)
        return queryset
