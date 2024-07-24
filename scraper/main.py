from news_drop import News
import os

key_instance = os.environ.get("key_instance")
language = os.environ.get("language")
country = os.environ.get("country")

test1 = News(max_drops=1000, period="1h", language=language, country=country)
test1.listening_drops(data=key_instance)
