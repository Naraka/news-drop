import requests
# docker stop $(docker ps -q)

def home():
    url = 'http://34.118.233.244:80/'
    response = requests.get(url)

    if response.status_code == 200:
        print(response.text)
    else:
        print('ERROR', response.status_code)


home()