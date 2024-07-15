from django.shortcuts import render
from drops.models import Drops
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import requests

BASE_URL = "http://34.118.234.43:80"
# BASE_URL = "http://127.0.0.1:80"

def superuser_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap

def server_error_view(request):
    return redirect('drops')

def health_check(request):
    return HttpResponse("OK", status=200)

def more_frequent_word(key_instance):
    url = f'{BASE_URL}/get_more_frequent_word/{key_instance}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return 'ERROR', response.status_code

def get_news_frequency(key_instance):
    url = f'{BASE_URL}/get_news_frequency/{key_instance}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return 'ERROR', response.status_code

def most_frequenttime(key_instance):
    url = f'{BASE_URL}/most_frequent_time/{key_instance}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return 'ERROR', response.status_code
def news_by_key(key_instance):
    url = f'{BASE_URL}/news/{key_instance}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return 'ERROR', response.status_code

@login_required
@superuser_required
def index(request):
    if request.method == "GET":
        drops = Drops.objects.filter(user=request.user)
        bar_data = more_frequent_word("outstanding_es_ES")
        news_frequency = get_news_frequency("outstanding_es_ES")
        most_frequent_time = most_frequenttime("outstanding_es_ES")
        news = news_by_key("outstanding_es_ES")


        return render(request, "index.html", {
            "data": drops,
            "bar_data":bar_data,
            "news_frequency":news_frequency,
            "most_frequent_time":most_frequent_time,
            "news":news,
        })
    else:
        return redirect("/")

