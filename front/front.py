import requests
# docker stop $(docker ps -q)

def post_bot(key_instance):
    url = 'http://127.0.0.1:80/post_bot/'
    data = {"key_instance": key_instance}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(response.text)
    else:
        print('ERROR', response.status_code)

list_example = ["madrid", "valencia"]

for i in list_example:
    post_bot(i)


