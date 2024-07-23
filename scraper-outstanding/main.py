from scraper_outstanding import News
import os
from dotenv import load_dotenv

try:
    load_dotenv()
except:
    pass

language = os.environ.get("language")
country = os.environ.get("country")
feed = News(language=language, country=country)
feed.listening_drops()
