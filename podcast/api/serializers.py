from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Podcast, RssItem

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']

class PodcastSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Podcast
        fields = ('__all__')

        name = serializers.CharField(max_length=100, required=True)
        url = serializers.URLField() 
        category = serializers.CharField()
        last_modified = serializers.DateTimeField(read_only=True)
        etag = serializers.CharField(read_only=True)

class RssItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RssItem
        fields = ('__all__')
        
        title = serializers.CharField(max_length=1024, required=True)
        pub_date = serializers.DateTimeField(read_only=True)
        desription = serializers.CharField(max_length=8192)
        item_url = serializers.URLField()
        episode_number = serializers.IntegerField()
        GUID = serializers.UUIDField(read_only=True)
        creator = serializers.CharField()
        