from news_drop.news_drop import News

test1 = News(max_drops=1, period="1h")
drop = test1.get_drops(data="banco santander")
print(drop)
test1.listening_drops(data="banco")