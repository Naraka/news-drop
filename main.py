from news_drop import News

test1 = News(max_drops=10, period="1d")
entrie = test1.get_drops(data="santander")
# print(entrie)

# print(test1._period)
print(test1._get_self_url)
# print(entrie)
# print(len(entrie))
