from django.shortcuts import render, redirect
from .forms import DropForm
from django.contrib.auth.decorators import login_required
from .models import Drops
from django.contrib import messages
from utils.config import superuser_required
from services.api_requests import get_news_frequency, more_frequent_word, most_frequenttime, news_by_key, delete_bot, post_bot

@login_required
@superuser_required
def index(request):
    if request.method == "GET":
        drops = Drops.objects.filter(user=request.user)
        return render(request, "drops/index.html", {
            "data": drops,
            "form": DropForm()
        })
    else:
        bot_form = DropForm(request.POST)
        if bot_form.is_valid():
            key_instance = bot_form.cleaned_data['key_instance']
            if Drops.objects.filter(key_instance=key_instance, user=request.user).exists():
                messages.error(request, 'Bot with this key instance already exists.')
                return redirect("drops")
            else:
                newbot = bot_form.save(commit=False)
                newbot.user = request.user
                newbot.key_instance = newbot.key_instance.lower()
                newbot.save()
                messages.success(request, 'Bot created successfully.')
                try:
                    post_bot(key_instance)
                except Exception as e:
                    messages.error(request, f'Error posting bot: {str(e)}')
                    return redirect("drops")
                
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
        interval = request.GET.get('interval', '1D')

        news = news_by_key(drop.key_instance)
        most_frequent_time = most_frequenttime(drop.key_instance, interval=interval)
        bar_data = more_frequent_word(drop.key_instance, interval=interval)
        news_frequency = get_news_frequency(drop.key_instance, interval=interval)


        context={
            "news":news,
            "data":data,
            "drop":drop,
            "bar_data":bar_data,
            "news_frequency":news_frequency,
            "most_frequent_time":most_frequent_time,
            "selected_interval": interval,
        }

        return render(request,"drops/detail.html",context)
    else:
        return redirect("drops")