from django.core.management.base import BaseCommand, CommandError
from podcast.api.models import Podcast, RssItem
import feedparser
from ._utils import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        return super().handle(*args, **options)
    
    def patch_podcast(self):
        pass

    def patch_rssItem(self):
        pass