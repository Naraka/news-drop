from news_drop import News

test1 = News(max_drops=2, period="1y")
entrie = test1.get_drops(data="santander")
# print(entrie)

# print(test1._period)
print(test1._get_self_url)
print(entrie)
