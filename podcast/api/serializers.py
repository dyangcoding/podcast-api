from ..users.models import ClubUser
from rest_framework import serializers
from .models import Podcast, RssItem
from django.core.paginator import Paginator

class ClubUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClubUser
        fields = ['display_name', 'email']  

class PodcastSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    category = serializers.CharField(source='get_category_display')
    
    class Meta:
        model = Podcast
        fields = ['id', 'name', 'base_url', 'image_url', 'category']
        
class RssItemRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    creator = PodcastSerializer()

    class Meta:
        model = RssItem
        fields = ['id', 'title', 'pub_date', 'description', \
                'item_url', 'enclosure', 'duration', 'summary', \
                'episode_number', 'likes', 'creator']

class RssItemListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    creator = PodcastSerializer()

    class Meta:
        model = RssItem
        fields = ['id', 'title', 'pub_date', 'item_url', 'duration', 'creator']