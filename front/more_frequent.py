import requests
def more_frequent_word(key_instance):
    url = f'http://127.0.0.1:80/get_more_frequent_word/{key_instance}'
    response = requests.get(url)

    if response.status_code == 200:
        print(response.json())
    else:
        print('ERROR', response.status_code)

more_frequent_word("argentina")