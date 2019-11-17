from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Podcast, RssItem
from django.core.paginator import Paginator

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']  

class PodcastSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Podcast
        fields = ('id', 'name', 'base_url', 'category')
        
class RssItemSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    creator = PodcastSerializer()

    class Meta:
        model = RssItem
        fields = ('id', 'title', 'pub_date', 'description', \
            'item_url', 'episode_number', 'creator')
        