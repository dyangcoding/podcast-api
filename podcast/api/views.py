from django.contrib.auth.models import User
from rest_framework import viewsets
from podcast.api.serializers import UserSerializer, RssItemSerializer, PodcastSerializer
from .models import RssItem, Podcast
from django.utils import timezone
from django.db.models import Q
from operator import or_
from functools import reduce

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

    date_querykey_mapper = {
        'Last 24': 1,
        'Past Week': 7,
        'Past Month': 30,
        'Past Year': 365
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
