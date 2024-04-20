from news_drop import News
import os

key_instance = os.environ.get("key_instance")

test1 = News(max_drops=1000, period="1h")
test1.listening_drops(data=key_instance)
