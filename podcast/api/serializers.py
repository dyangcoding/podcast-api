from django.contrib.auth.models import User
from rest_framework import serializers, pagination
from .models import Podcast, RssItem
from django.core.paginator import Paginator

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']  

class RssItemSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = RssItem
        fields = ('id', 'title', 'pub_date', 'description', 'item_url', 'episode_number')

class PodcastSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    items = serializers.SerializerMethodField('paginated_items')
    #items = RssItemSerializer(many=True)
    class Meta:
        model = Podcast
        fields = ('id', 'name', 'base_url', 'category', 'items')
    
    def paginated_items(self, obj):
        #items = RssItem.objects.filter(creator=obj)
        """ paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(items, self.context['request'])
        serializer = RssItemSerializer(page, many=True, context={'request': self.context['request']}) """

        page_size = self.context['request'].query_params.get('size') or 10
        paginator = Paginator(obj.items.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1

        items_in_p = paginator.page(page)
        serializer = RssItemSerializer(items_in_p, many=True)
        return serializer.data
        #return paginator.get_paginated_response(serializer.data).data
        
        