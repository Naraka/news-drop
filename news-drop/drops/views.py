from django.shortcuts import render, redirect
from .forms import DropForm
from django.contrib.auth.decorators import login_required
from .models import Drops
from django.contrib import messages
from utils.config import superuser_required
from services.api_requests import get_news_frequency, more_frequent_word, most_frequenttime, news_by_key, delete_bot, post_bot, sentiment

@login_required
@superuser_required
def index(request):
    if request.method == "GET":
        drops = Drops.objects.filter(user=request.user)
        return render(request, "drops/index.html", {
            "data": drops,
        })
    else:
        bot_form = DropForm(request.POST)
        if bot_form.is_valid():
            key_instance = bot_form.cleaned_data['key_instance']
            country_form = bot_form.cleaned_data['country']
            if bot_form.cleaned_data['country'] == "us":
                country = "US"
                language = "en"
            elif bot_form.cleaned_data['country'] == "es":
                country = "ES"
                language = "es"
            else : raise "bad country"
            if Drops.objects.filter(key_instance=key_instance, user=request.user).exists():
                messages.error(request, 'Bot with this key instance already exists.')
                return redirect("drops")
            else:
                newbot = bot_form.save(commit=False)
                newbot.user = request.user
                newbot.key_instance = newbot.key_instance.lower()
                try:
                    newbot.save()
                    messages.success(request, 'Bot created successfully.')
                    try:
                        post_bot(key_instance=key_instance, language=language, country=country)
                    except Exception as e:
                        messages.error(request, f'Error posting bot: {str(e)}')
                        return redirect("drops")
                except ValueError as e:
                    messages.error(request, str(e))
                
                return redirect("drops")
        else:
            messages.error(request, 'Invalid form submission.')
            return redirect("drops")


@login_required
@superuser_required
def delete_drop(request, drop_id):
    drop = Drops.objects.get(id=drop_id, user=request.user)
    drop.delete()
    if not Drops.objects.filter(key_instance=drop.key_instance).exists():
        delete_bot(drop.key_instance)
        return redirect("drops")    
    else:
        return redirect("drops")

@login_required
@superuser_required
def detail(request, drop_id):
    if request.method == "GET":
        drop = Drops.objects.get(id=drop_id, user=request.user)
        data = Drops.objects.filter(user=request.user)
        country_get = Drops.objects.get(id=drop_id, user=request.user).country
        if country_get == "us":
            selected_country = "US"
            selected_language = "en"
        elif country_get == "es":
            selected_country = "ES"
            selected_language = "es"
        else : raise "bad country"
        selected_interval = request.GET.get('interval', '1M')

        bar_data = more_frequent_word(drop.key_instance, interval=selected_interval, language=selected_language, country=selected_country)
        sentiment_data = sentiment(drop.key_instance, language=selected_language, country=selected_country) 
        news_frequency = get_news_frequency(drop.key_instance, interval=selected_interval, language=selected_language, country=selected_country)
        most_frequent_time = most_frequenttime(drop.key_instance, interval=selected_interval, language=selected_language, country=selected_country)
        news = news_by_key(drop.key_instance, language=selected_language, country=selected_country)

        context={
            "drop":drop,
            "data":data,
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
        }

        return render(request,"drops/detail.html",context)
    else:
        return redirect("drops")