# Podcast Backend API

###### **Introduction**
This API serves [Podcast Club](http://podcastclub.net) a daily updated RSS Feed to inform users new posted episodes 
of the topic IT, Entrepreneurship, finance.

The backend Api contains mainly 2 Resources as described below and currently only supports HTTP GET method.

* Note: The base Url to the backend Api: http://fathomless-beyond-28426.herokuapp.com

**Resources**

* api/rssItems 3425 items (Nov. 2019)
* api/podcasts 16 podcasts (Nov. 2019)

**Routes**

* get api/rssItems
* get api/rssItems/1
* get api/podcasts
* get api/podcasts/1

Items
----
Get http://fathomless-beyond-28426.herokuapp.com/api/rssItems
```json
[
  {
    "id": 3445,
    "title": "Ray Dalio - How to embrace conflict",
    "pub_date": "2019-11-26T03:00:00Z",
    "description": "Want to improve any idea? Find someone who disagrees with it. This is something legendary investor Ray Dalio knows. But there’s a difference between constructive and destructive conflict – and Dalio is a master at spotting the difference. In constructive conflict, a team has a shared goal, whether or not",
    "item_url": "https://chtbl.com/track/E341G/rss.art19.com/episodes/258ad7ff-cf92-45d2-acf1-94a9733a5fd8.mp3",
    "episode_number": 52,
    "creator": {
      "id": 7,
      "name": "Masters of Scale",
      "base_url": "mastersofscale.com",
      "category": "PodcastCategory.Entrepreneurship"
    }
  },
  {
    "id": 3442,
    "title": "Should I Take Social Security as a Lump Sum? (Hour 3)",
    "pub_date": "2019-11-25T22:30:00Z",
    "description": "Debt, Retirement As heard on this episode: ButcherBox: http://bit.ly/2JdWlez  LinkedIn: http://bit.ly/2JdWlez  Tools to get you started:  Debt Calculator: http://bit.ly/2QIoSPV Insurance Coverage Checkup: http://bit.ly/2BrqEuo Complete Guide to Budgeting: http://bit.ly/2QEyonc Interview Guide: http://bit.ly/2BuGnZE Check out other podcasts in the Ramsey Network: http://bit.ly/2JgzaQR     ",
    "item_url": "http://daveramsey.ramsey.libsynpro.com/11252019-h3",
    "episode_number": 10843,
    "creator": {
      "id": 10,
      "name": "The Dave Ramsey Show",
      "base_url": "www.daveramsey.com",
      "category": "PodcastCategory.Finance"
    }
  }
] 
```

Item
----
Get http://fathomless-beyond-28426.herokuapp.com/api/rssItems/:id
```json
{
  "id": 3445,
  "title": "Ray Dalio - How to embrace conflict",
  "pub_date": "2019-11-26T03:00:00Z",
  "description": "Want to improve any idea? Find someone who disagrees with it. This is something legendary investor Ray Dalio knows. But there’s a difference between constructive and destructive conflict – and Dalio is a master at spotting the difference. In constructive conflict, a team has a shared goal, whether or not",
  "item_url": "https://chtbl.com/track/E341G/rss.art19.com/episodes/258ad7ff-cf92-45d2-acf1-94a9733a5fd8.mp3",
  "episode_number": 52,
  "creator": {
    "id": 7,
    "name": "Masters of Scale",
    "base_url": "mastersofscale.com",
    "category": "PodcastCategory.Entrepreneurship"
  }
}
```

Podcasts
----
Get http://fathomless-beyond-28426.herokuapp.com/api/podcasts
```json
 [
  {
    "id": 2,
    "name": "Djangochat",
    "base_url": "djangochat.com",
    "category": "PodcastCategory.IT"
  },
  {
    "id": 5,
    "name": "Friday afternoon deploy",
    "base_url": "friday.hirelofty.com",
    "category": "PodcastCategory.IT"
  }
]
```

Podcast
----
Get http://fathomless-beyond-28426.herokuapp.com/api/podcasts/:id
```json
{
  "id": 2,
  "name": "Djangochat",
  "base_url": "djangochat.com",
  "category": "PodcastCategory.IT"
} 
```

###### **Author**
* Dong Yang 
* Email: tu295t.dy@gmail.com
