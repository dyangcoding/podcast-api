from django.core.management.base import BaseCommand, CommandError
from podcast.api.models import Podcast, RssItem
import feedparser
from django.utils.html import strip_tags
from datetime import datetime
from time import mktime
import uuid
from django.utils.timezone import make_aware

"""
a basic map to populate db
each podcast name as key contains following entry as value
    base_url
    rss_link
    category
"""
podcasts = {
    'Talk python to me': [
        'https://talkpython.fm',
        'https://talkpython.fm/episodes/rss',
        1
    ],
    'Djangochat': [
        'https://djangochat.com/',
        'https://feeds.simplecast.com/WpQaX_cs',
        1
    ],
    'Python podcast init': [
        'https://www.pythonpodcast.com/',
        'https://www.pythonpodcast.com/feed/mp3/',
        1
    ],
    'Test & code': [
        'https://testandcode.com/',
        'https://testandcode.com/rss',
        1
    ],
    'Friday afternoon deploy': [
        'https://friday.hirelofty.com',
        'https://feeds.simplecast.com/7if5txYU',
        1
    ],
    'Beyond the todo list': [
        'https://beyondthetodolist.com',
        'https://beyondthetodolist.com/rss',
        2
    ],
    'Masters of Scale': [
        'https://mastersofscale.com/',
        'https://rss.art19.com/masters-of-scale',
        2
    ],
    'Saas interviews with ceos, startups, founders': [
        'https://nathanlatkathetop.libsyn.com/',
        'https://nathanlatkathetop.libsyn.com/rss',
        2
    ],
    'How i Build this': [
        'https://www.npr.org/podcasts/510313/how-i-built-this?t=1573735345664',
        'https://www.npr.org/rss/podcast.php?id=510313',
        2
    ],
    'The Dave Ramsey Show': [
        'https://www.daveramsey.com/show/podcasts',
        'http://daveramsey.ramsey.libsynpro.com/rss',
        3
    ],
    'Money for the Rest of us': [
        'https://moneyfortherestofus.com',
        'https://rss.art19.com/money-for-the-rest-of-us',
        3
    ]
}
    
class Command(BaseCommand):
    """
    load all rss feed items from the given podcast feed,
    loaded data would be populated into database

    this command should only be executed once for each podcast
    after the database has been initialized

    also check if the given podcast already exists if
    the list of podcast has been constantly changing

    """
    @staticmethod
    def to_desc(text, size):
        """
        remove html tags and truncate the given string 
        :text given string may contain html tags
        :size max output size, 50 for item description, and 100 for podcast 
        """
        desc = strip_tags(text)
        splitted = desc.split()
        desc = ' '.join(splitted[:size]) if len(splitted) > size else desc
        return desc

    @staticmethod
    def to_aware_datetime(date_parsed):
        # converts date time tuple to datatime.datetime object
        date = datetime.fromtimestamp(mktime(date_parsed))
        # converts naive datetime object (without timezone info) to 
        # the one that has timezone info
        return make_aware(date)
        
    @staticmethod
    def to_item_url(item):
        """
        get the item link 
        if the link attribute is not present, find the link
        from the 'enclosures' attribute
        """
        if hasattr(item, 'link'):
            return item.link
        return item.enclosures[0].href if hasattr(item, 'enclosures') else None

    @staticmethod
    def get_epi_number(item):
        return item.itunes_episode if hasattr(item, 'itunes_episode') else None

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
            pd.description = Command.to_desc(parsed_data.feed.description, 100)
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
                pub_date = Command.to_aware_datetime(item.published_parsed),
                description = Command.to_desc(item.summary, 50), 
                item_url = Command.to_item_url(item),
                episode_number = Command.get_epi_number(item), 
                GUID = uuid.uuid4(),
                creator = pd)

    
    
    

