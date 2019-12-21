from django.contrib.auth.models import User
from rest_framework import viewsets, status
from podcast.api.serializers import UserSerializer, RssItemSerializer, PodcastSerializer
from .models import RssItem, Podcast
from django.utils import timezone
from django.db.models import Q
from operator import or_
from functools import reduce
from rest_framework.response import Response
from rest_framework.exceptions import APIException

class MethodUnavailable(APIException):
    status_code = 503
    default_detail = 'Patch Method is only available through podcastclub.net.'
    default_code = 'method_unavailable'

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

class UpdateModelMixin(object):
    """
    Update a model instance.
    """
    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class RssItemViewSet(UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows rss feed items to be viewed or 
    updated through partial update.
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
    
    def partial_update(self, request, *args, **kwargs):
        try: 
         if (request.data['upVote']):
            item = self.get_object()
            item.upVote()
        except KeyError:
            raise MethodUnavailable
        return super().partial_update(request, *args, **kwargs)
        
