from django.core.management.base import BaseCommand, CommandError
from podcast.api.models import Podcast, RssItem
import feedparser
from ._utils import *
from ._podcastsRef import podcasts
import uuid
    
class Command(BaseCommand):
    """
    load all rss feed items from the given podcast feed,
    loaded data would be populated into database

    this command should only be executed once for each podcast
    after the database has been initialized

    also check if the given podcast already exists if
    the list of podcast has been constantly changing

    """
    def handle(self, *args, **options):
        for name, data in podcasts.items():
            if Podcast.objects.filter(name=name).exists(): 
                print('Skip podcast {}, already exists in the db'
                        .format(name))
                continue
            rss_link = data[1]
            d = feedparser.parse(rss_link)
            self.collect_podcast(name, data, d)
            self.collect_rssItem(name, d)

    def collect_podcast(self, pc_name, pc_data, parsed_data):
        base_url, rss_link, category = pc_data[0], pc_data[1], pc_data[2]
        pd = Podcast()
        pd.name = pc_name
        pd.base_url = base_url.split('://')[1].split('/')[0]
        pd.rss_link = rss_link
        pd.category = category
        if hasattr(parsed_data.feed, 'description'):
            pd.description = to_desc(parsed_data.feed.description, 100)
        if hasattr(parsed_data, 'etag'):
            pd.etag = parsed_data.etag
        if hasattr(parsed_data, 'modified'):
            pd.last_modified = parsed_data.modified
        pd.save()
    
    def collect_rssItem(self, pc_name, parsed_data):
        pd = Podcast.objects.filter(name=pc_name).first()
        if pd is None:
            raise CommandError('Podcast with name {} does not exist'.format(pc_name))
        for item in parsed_data.entries:
            RssItem.objects.create(title = item.title, 
                pub_date = to_aware_datetime(item.published_parsed),
                description = to_desc(item.summary, 50), 
                item_url = to_item_url(item),
                episode_number = get_epi_number(item), 
                GUID = uuid.uuid4(),
                creator = pd)
    
    

