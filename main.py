from news_drop import News

test1 = News(max_drops=10, period="1h")
# entrie = test1.get_drops(data="santander")

db = []
test1.listening_drops(data_set=db, data="banco santander")

