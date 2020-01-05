from django.utils.html import strip_tags
from datetime import datetime
from time import mktime
from django.utils.timezone import make_aware

def to_desc(text, size):
    """
    remove html tags and truncate the given string 
    
    :text given string may contain html tags
    :size max output size, 50 for item description, 100 for podcast 
    """
    desc = strip_tags(text)
    splitted = desc.split()
    desc = ' '.join(splitted[:size]) if len(splitted) > size else desc
    return desc

def to_aware_datetime(date_parsed):
    """
    converts date time tuple to datatime.datetime object
    serve naive datetime object (without timezone info) to 
    the one that has timezone info
    
    :date_parsed
    """
    date = datetime.fromtimestamp(mktime(date_parsed))
    return make_aware(date)
    
def to_item_url(item):
    """
    get the item link 

    :item
    """
    
    return item.link if hasattr(item, 'link') else None
    
def to_item_enclosure(item):
    """
    get the item enclosure

    :item
    """
    return item.enclosures[0].href if hasattr(item, 'enclosures') else None

def to_summary(item):
    """
    get item summary

    :item
    """

    return item.itunes_summary if hasattr(item, 'itunes_summary') else None

def to_image(podcast):
    """

    """

    return

def to_duration(item):
    """
    get the item enclosure duration

    :return duration in second
    """

def get_epi_number(item):
    return item.itunes_episode if hasattr(item, 'itunes_episode') else None