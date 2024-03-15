import feedparser

# Really Simple Syndication, Atom
RSS_URL = "https://news.google.com/rss"


class News:

    def __init__(self, max_drops=5):
        self.max_drops = max_drops

    def get_drops(self, data: str):
        url = RSS_URL + f"/search?q={data}"
        return self._get_feeds(url)

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
