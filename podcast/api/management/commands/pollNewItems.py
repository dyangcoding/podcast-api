from django.core.management.base import BaseCommand, CommandError
from podcast.api.models import Podcast, RssItem
import feedparser

class Command(BaseCommand):
    def handle(self, *args, **options):
        podcasts = Podcast.objects.values_list(
            'id', 'etag', 'last_modified', 'rss_link')
        for data in podcasts:
            etag = data[1]
            last_modified = data[2]
            d = feedparser.parse(data[3], etag=etag, modified=last_modified)
            if d.status == 304:
                continue
            # need to update etag and modified field
            self.append_items(d, data[0])
            
    def append_items(self, parsed_data, p_id):
        latest_item = RssItem.objects.filter(creator=p_id).latest()
        for item in parsed_data.entries:
            pass
