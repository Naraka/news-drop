from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from services.api_requests import APIClient
from django.views.decorators.cache import cache_page, cache_control

API = APIClient()

def server_error_view(request):
    return redirect('/')

def health_check(request):
    return HttpResponse("OK", status=200)

@cache_page(60 * 15)
@cache_control(max_age=3600) 
def index(request):
    if request.method == "GET":
        key_instance = "outstanding"

        selected_interval = request.GET.get('interval', '7D')
        selected_language  = request.GET.get('language', 'es')
        selected_country  = request.GET.get('country', 'ES')

        bar_data = API.more_frequent_word(key_instance=key_instance, interval=selected_interval, language=selected_language, country=selected_country)
        # sentiment_data = API.sentiment(key_instance=key_instance, language=selected_language, country=selected_country) 
        news_frequency = API.get_news_frequency(key_instance=key_instance, interval=selected_interval, language=selected_language, country=selected_country)
        most_frequent_time = API.most_frequent_time(key_instance=key_instance, interval=selected_interval, language=selected_language, country=selected_country)
        news = API.news_by_key(key_instance=key_instance, language=selected_language, country=selected_country)

        return render(request, "index.html", {
            "bar_data": bar_data,
            "news_frequency": news_frequency,
            "most_frequent_time": most_frequent_time,
            "news": news,
            # "sentiment_data": sentiment_data,
            "selected_interval": selected_interval,
            "selected_country": selected_country,
            "selected_language": selected_language,
            "selected_interval_code": selected_interval,
            "selected_country_code": selected_country,
            "selected_language_code": selected_language,
        })
    else:
        return redirect("/")

