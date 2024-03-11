import requests

# Really Simple Syndication, Atom
RSS_URL = "https://news.google.com/rss"

class News():

    def __init__(self):
        pass


    def get_drops(self, data:str):
        url = RSS_URL + f"/search?q={data}"
        return self.get_xml(url)

    
    def get_xml(self, url):
        return requests.get(url).content
        
    















