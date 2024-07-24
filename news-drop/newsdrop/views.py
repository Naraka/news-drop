from django.shortcuts import render
from drops.models import Drops
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
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
        key_instance = "outstanding"

        selected_interval = request.GET.get('interval', '7D')
        selected_language  = request.GET.get('language', 'es')
        selected_country  = request.GET.get('country', 'ES')

        bar_data = more_frequent_word(key_instance, interval=selected_interval, language=selected_language, country=selected_country)
        sentiment_data = sentiment(key_instance, language=selected_language, country=selected_country) 
        news_frequency = get_news_frequency(key_instance, interval=selected_interval, language=selected_language, country=selected_country)
        most_frequent_time = most_frequenttime(key_instance, interval=selected_interval, language=selected_language, country=selected_country)
        news = news_by_key(key_instance, language=selected_language, country=selected_country)

        drops = Drops.objects.filter(user=request.user)

        return render(request, "index.html", {
            "data": drops,
            "bar_data": bar_data,
            "news_frequency": news_frequency,
            "most_frequent_time": most_frequent_time,
            "news": news,
            "sentiment_data": sentiment_data,
            "selected_interval": selected_interval,
            "selected_country": selected_country,
            "selected_language": selected_language,
            "selected_interval_code": selected_interval,
            "selected_country_code": selected_country,
            "selected_language_code": selected_language,
        })
    else:
        return redirect("/")

