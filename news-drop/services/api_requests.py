from utils.config import BASE_URL
import requests


def more_frequent_word(key_instance, interval='1D', language="en", country="US"):
    url = f'{BASE_URL}/get_more_frequent_word/{key_instance}'
    params = {"interval": interval,
              "language": language,
              "country": country              
              }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return 'ERROR', response.status_code
    except requests.exceptions.RequestException as e:
        return 'ERROR', str(e)

def sentiment(key_instance, language="en", country="US"):
    url = f'{BASE_URL}/sentiment/{key_instance}'
    params = {"language": language,
              "country": country              
              }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return 'ERROR', response.status_code
    except requests.exceptions.RequestException as e:
        return 'ERROR', str(e)

def get_news_frequency(key_instance, interval='1D', language="en", country="US"):
    url = f'{BASE_URL}/get_news_frequency/{key_instance}'
    params = {"interval": interval,
              "language": language,
              "country": country              
              }
    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return 'ERROR', response.status_code
    except requests.exceptions.RequestException as e:
        return 'ERROR', str(e)

def most_frequenttime(key_instance, interval='1D', language="en", country="US"):
    url = f'{BASE_URL}/most_frequent_time/{key_instance}'
    params = {"interval": interval,
              "language": language,
              "country": country              
              }
    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return 'ERROR', response.status_code
    except requests.exceptions.RequestException as e:
        return 'ERROR', str(e)
def news_by_key(key_instance, language="en", country="US"):
    url = f'{BASE_URL}/news/{key_instance}'
    params = {"language": language,
          "country": country              
          }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return 'ERROR', response.status_code
    
def delete_bot(key_instance):
    url = f'{BASE_URL}/delete_bots/{key_instance}'
    response = requests.delete(url)

    if response.status_code == 200:
        print(response.text)
    else:
        print('ERROR', response.status_code)

def post_bot(key_instance, language="en", country="US"):
    url = f'{BASE_URL}/post_bot/'
    data = {
        "key_instance": key_instance,
        "language": language,
        "country": country,
            }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.text
    else:
        return response.status_code