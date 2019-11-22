"""
a basic map to populate db
each podcast name served as a key which contains 
following entry as value
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
    ],
    'Mad Fientist': [
        'https://www.madfientist.com',
        'https://www.madfientist.com/feed',
        3
    ],
    '2 Frugal Dudes': [
        'https://2frugaldudes.com',
        'https://2frugaldudes.com/feed/podcast',
        3
    ],
    'Maven Money Personal Finance Podcast': [
        'https://mavenmoney.libsyn.com',
        'http://mavenmoney.libsyn.com/rss',
        3
    ],
    'Retirement Lifestyle Advocates': [
        'http://www.everythingfinancialradio.com',
        'http://www.everythingfinancialradio.com/feed/podcast/',
        3
    ]
}