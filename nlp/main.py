from google.cloud import language_v1
import requests

BASE_URL = "http://127.0.0.1:80"


def get_news():
    url = f'{BASE_URL}/news'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return 'ERROR', response.status_code
    except requests.exceptions.RequestException as e:
        return 'ERROR', str(e)
    

def analyze(news):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=news, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    return client.analyze_sentiment(request={"document": document})

for n in get_news():
    print(analyze(n["title"]).document_sentiment, n["title"])