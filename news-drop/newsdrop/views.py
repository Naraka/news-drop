from django.shortcuts import render
from drops.models import Drops
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import requests
from utils.config import BASE_URL


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

def more_frequent_word(key_instance, interval='1D'):
    url = f'{BASE_URL}/get_more_frequent_word/{key_instance}'
    params = {'interval': interval}

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return 'ERROR', response.status_code
    except requests.exceptions.RequestException as e:
        return 'ERROR', str(e)

def get_news_frequency(key_instance, interval='1D'):
    url = f'{BASE_URL}/get_news_frequency/{key_instance}'
    params = {'interval': interval}

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return 'ERROR', response.status_code
    except requests.exceptions.RequestException as e:
        return 'ERROR', str(e)

def most_frequenttime(key_instance, interval='1D'):
    url = f'{BASE_URL}/most_frequent_time/{key_instance}'
    params = {'interval': interval}

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return 'ERROR', response.status_code
    except requests.exceptions.RequestException as e:
        return 'ERROR', str(e)
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
        key_instance = "outstanding_es_ES"  # Ejemplo de key_instance fija, puedes obtenerla dinámicamente según tus necesidades

        # Obtener parámetros del filtro del front-end (ejemplo)
        interval = request.GET.get('interval', '1D')

        # Llamar a las funciones que envían solicitudes a FastAPI
        bar_data = more_frequent_word(key_instance, interval=interval)
        news_frequency = get_news_frequency(key_instance, interval=interval)
        most_frequent_time = most_frequenttime(key_instance, interval=interval)
        news = news_by_key(key_instance)

        # Obtener objetos de Django relacionados con el usuario autenticado
        drops = Drops.objects.filter(user=request.user)

        return render(request, "index.html", {
            "data": drops,
            "bar_data": bar_data,
            "news_frequency": news_frequency,
            "most_frequent_time": most_frequent_time,
            "news": news,
            "selected_interval": interval,
        })
    else:
        return redirect("/")

