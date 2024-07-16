from django.shortcuts import render
from drops.models import Drops
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from services.api_requests import *
from utils.config import superuser_required

def server_error_view(request):
    return redirect('drops')

def health_check(request):
    return HttpResponse("OK", status=200)

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

