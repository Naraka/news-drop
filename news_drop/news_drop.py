import feedparser

# Really Simple Syndication, Atom
RSS_URL = "https://news.google.com/rss"


class News:

    def __init__(self, max_drops=None, period=None,
                 language="es", country="ES"):

        self.max_drops = max_drops
        self.period = period
        self.language = language
        self.country = country

    def get_drops(self, data: str):
        self._url = "{}/search?q={}{}&hl={}&gl={}&ceid={}:{}".format(RSS_URL,
                                                                     data,
                                                                     self._period,
                                                                     self.language,
                                                                     self.country,
                                                                     self.country,
                                                                     self.language)

        return self._get_feeds(self._url)

    def _get_feeds(self, url: str):
        feeds = feedparser.parse(url)
        serialized_feeds = list(map(self._serialization, feeds.entries[:self.max_drops]))
        return serialized_feeds

    def _serialization(self, entrie):
        json = {
            "title": self._title_clean(entrie.title),
            "link": entrie.link,
            "published_date": entrie.published,
            "description": self._description_clean(entrie.description),
            "source": entrie.source.title,
        }
        return json

    def _description_clean(self, description):
        start = description.find('<a')
        end = description.find('</a>')

        if start != -1 and end != -1:
            description_tags = description[start:end]

            first_gt = description_tags.find('>')

            if first_gt != -1:
                clean_text = description_tags[first_gt + 1:]

                return clean_text
        return None

    def _title_clean(self, title):
        index_hyphen = title.rfind('-')
        if index_hyphen != -1:
            return title[:index_hyphen].strip()
        else:
            return title.strip()

    @property
    def _period(self):
        if self.period is not None:
            period = f'%20when%3A{self.period}'
        return period

    @property
    def _get_self_url(self):
        return self._url
