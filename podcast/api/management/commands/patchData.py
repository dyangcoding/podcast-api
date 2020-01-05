from django.core.management.base import BaseCommand, CommandError
from podcast.api.models import Podcast, RssItem
import feedparser
from ._utils import to_duration, to_item_enclosure, to_item_url

class Command(BaseCommand):
    """
    one time data patch command due to model modification
    
    new db fields:

    Podcast: image_url
    RssItem: summary, duration, enclosure

    """
    def handle(self, *args, **options):
        for podcast in Podcast.objects.all():
            rss_link = podcast.rss_link
            d = feedparser.parse(rss_link)
            if hasattr(d.feed, 'image'):
                print('Patch podcast {} image data.'.format(podcast.name))
                podcast.image_url = d.feed.image.href
                podcast.save()
            else:
                print('Podcast {} has no image data.'.format(podcast.name))
            self.patch_rssItem(d)

    def patch_rssItem(self, parsed_data):
        """
        update each rss item 
        """
        print('Patch Rss Item..')
        for item in parsed_data.entries:
            item_instance = RssItem.objects.filter(title=item.title).first()
            if item_instance is None:
                print('No Item {} exists within database.'.format((item.title).encode('utf-8')))
                continue
            item_instance.summary = item.summary
            # seperate item link and enclosure 
            item_instance.item_url = to_item_url(item)
            item_instance.duration = to_duration(item)
            item_instance.enclosure = to_item_enclosure(item)
            item_instance.save()
        print('Done.')