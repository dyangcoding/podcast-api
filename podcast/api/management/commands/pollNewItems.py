from django.core.management.base import BaseCommand, CommandError
from podcast.api.models import Podcast, RssItem
import feedparser
from ._utils import *
import uuid

class Command(BaseCommand):
    def handle(self, *args, **options):
        # need the object instance to update etag and last_modified
        podcasts = Podcast.objects.all()
        for p in podcasts:
            etag = p.etag
            last_modified = p.last_modified
            d = feedparser.parse(p.rss_link, etag=etag, modified=last_modified)
            if d.status == 304:
                continue
            print('Podcast {} has updated.'.format(p.name))
            if hasattr(d, 'etag'):
                p.etag = d.etag
            if hasattr(d, 'modified'):
                p.last_modified = d.modified
            p.save()
            self.append_items(d, p)
            
    def append_items(self, parsed_data, podcast):
        latest_item = RssItem.objects.filter(creator=podcast).latest('pub_date')
        for item in parsed_data.entries:
            item_date = to_aware_datetime(item.published_parsed)
            if item_date > latest_item.pub_date:
                print('Append new item into podcast {}'.format(podcast.name))
                RssItem.objects.create(title = item.title, 
                    pub_date = item_date,
                    description = to_desc(item.summary, 50), 
                    item_url = to_item_url(item),
                    episode_number = get_epi_number(item), 
                    GUID = uuid.uuid4(),
                    creator = podcast
                )
