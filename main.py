from news_drop import News

test1 = News(max_drops=10)
entrie = test1.get_drops(data="bancaja")[0]
print("entrie", entrie)