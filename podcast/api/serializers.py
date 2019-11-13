from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Podcast, RssItem

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
    items = RssItemSerializer(many=True, read_only=True)
    class Meta:
        model = Podcast
        fields = ('id', 'name', 'url', 'category', 'items')
        
        