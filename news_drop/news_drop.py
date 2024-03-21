import feedparser

# Really Simple Syndication, Atom
RSS_URL = "https://news.google.com/rss"


class News:

    def __init__(self, max_drops=5, period=None):
        self.max_drops = max_drops
        self.period = period

    def get_drops(self, data: str):
        self._url = RSS_URL + f"/search?q={data}+{self._period}"
        return self._get_feeds(self._url)

    def _get_feeds(self, url: str):

        feeds = feedparser.parse(url)

        def _serialization(entrie):
            json = {
                "title": entrie.title,
                "link": entrie.link,
                "published_date": entrie.published,
                "description": entrie.description,
                "source": entrie.source,
            }
            return json

        serialized_feeds = list(map(_serialization, feeds.entries))
        return serialized_feeds

    @property
    def _period(self):
        if self.period is not None:
            period = f'%20when%3A{self.period}'
        return period

    @property
    def _get_self_url(self):
        return self._url
