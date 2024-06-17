from django.shortcuts import render
import requests


def index(request):
    url = "http://127.0.0.1:80/get_bots/"
    response = requests.get(url=url)

    if response.status_code == 200:
        data = response.json()
    else:
        data = {"error":response.status_code}

    return render(request,"drops/index.html",{"data":data})

