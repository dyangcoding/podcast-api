from django.contrib.auth.models import User
from rest_framework import serializers
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

    class Meta:
        model = Podcast
        fields = ('id', 'name', 'base_url', 'category', 'items')
    
    def paginated_items(self, obj):
        page_size = self.context['request'].query_params.get('size') or 10
        paginator = Paginator(obj.items.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1
        items_in_p = paginator.page(page)
        serializer = RssItemSerializer(items_in_p, many=True)
        return serializer.data
        
        