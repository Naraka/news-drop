from utils.config import BASE_URL
import requests

class APIClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def _get(self, endpoint, params):
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return 'ERROR', response.status_code
        except requests.exceptions.RequestException as e:
            return 'ERROR', str(e)

    def _post(self, endpoint, data):
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return response.text
            else:
                return 'ERROR', response.status_code
        except requests.exceptions.RequestException as e:
            return 'ERROR', str(e)

    def _delete(self, endpoint):
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.delete(url)
            if response.status_code == 200:
                return response.text
            else:
                return 'ERROR', response.status_code
        except requests.exceptions.RequestException as e:
            return 'ERROR', str(e)

    def more_frequent_word(self, key_instance, interval='1D', language="en", country="US"):
        params = {"interval": interval, "language": language, "country": country}
        return self._get(f'get_more_frequent_word/{key_instance}', params)

    def sentiment(self, key_instance, language="en", country="US"):
        params = {"language": language, "country": country}
        return self._get(f'sentiment/{key_instance}', params)

    def get_news_frequency(self, key_instance, interval='1D', language="en", country="US"):
        params = {"interval": interval, "language": language, "country": country}
        return self._get(f'get_news_frequency/{key_instance}', params)

    def most_frequent_time(self, key_instance, interval='1D', language="en", country="US"):
        params = {"interval": interval, "language": language, "country": country}
        return self._get(f'most_frequent_time/{key_instance}', params)

    def news_by_key(self, key_instance, language="en", country="US"):
        params = {"language": language, "country": country}
        return self._get(f'news/{key_instance}', params)

    def delete_bot(self, key_instance):
        return self._delete(f'delete_bots/{key_instance}')

    def post_bot(self, key_instance, language="en", country="US"):
        data = {"key_instance": key_instance, "language": language, "country": country}
        return self._post('post_bot/', data)
