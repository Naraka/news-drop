import feedparser

# Really Simple Syndication, Atom
RSS_URL = "https://news.google.com/rss"

class News:

    def __init__(self, max_drops=5):
        self.max_drops = max_drops


    def get_drops(self, data:str):
        url = RSS_URL + f"/search?q={data}"
        return self.get_feeds(url)


    def get_feeds(self, url:str):

        feeds = feedparser.parse(url)

        box = []
        for feed in feeds.entries:
            box.append(feed)
            if len(box) == self.max_drops:
                break
    
        return box

    def serialization(self, entrie):
        json = {
            "title" : entrie.title,
            "link" : entrie.link,
            "published" : entrie.published
        }
        return json