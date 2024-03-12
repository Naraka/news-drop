from news_drop import News

test1 = News(max_drops=1)

entrie = test1.get_drops(data="nba")[0]

json = {
    "title" : entrie.title,
    "link" : entrie.link,
    "published" : entrie.published
}

print(json)