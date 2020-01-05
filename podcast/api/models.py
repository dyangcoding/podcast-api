from django.db import models
from enum import Enum, unique

@unique
class PodcastCategory(Enum):
    IT = 1
    Entrepreneurship = 2
    Finance = 3

class Podcast(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=4096, default=None)
    base_url = models.URLField(default=None)
    rss_link = models.URLField(default=None)
    image_url = models.TextField(default=None, null=True)
    category = models.IntegerField(choices= 
                [(tag.value, tag) for tag in PodcastCategory])
    last_modified = models.CharField(max_length=100, null=True)
    etag = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class RssItem(models.Model):
    title = models.CharField(max_length=1024)
    pub_date = models.DateTimeField()
    description = models.CharField(max_length=8192)
    item_url = models.TextField(default=None, null=True)
    summary = models.TextField(default=None, null=True)
    duration = models.IntegerField(default=0)
    enclosure = models.TextField(default=None, null=True)
    episode_number = models.IntegerField(default=0, null=True)
    likes = models.IntegerField(default=0)
    GUID = models.UUIDField(editable=False)
    creator = models.ForeignKey('Podcast', related_name='items', on_delete=models.CASCADE)

    def upVote(self):
        self.likes = self.likes + 1
        self.save()
