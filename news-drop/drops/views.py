from django.shortcuts import render, redirect
import requests
from .forms import DropForm
from django.contrib.auth.decorators import login_required
from .models import Drops
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def superuser_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap

def post_bot(key_instance):
    url = 'http://34.118.233.244:80/post_bot/'
    data = {"key_instance": key_instance}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.text
    else:
        return response.status_code

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


def delete_bot(key_instance):
    url = f'http://34.118.233.244:80/delete_bots/{key_instance}'
    response = requests.delete(url)

    if response.status_code == 200:
        print(response.text)
    else:
        print('ERROR', response.status_code)

@login_required
@superuser_required
def delete_drop(request, drop_id):
    drop = Drops.objects.get(id=drop_id, user=request.user)
    drop.delete()

    if Drops.objects.filter(key_instance=drop.key_instance).exists():
        return redirect("drops")    
    else:
        print(drop.key_instance)
        delete_bot(drop.key_instance)
        return redirect("drops")






def news_by_key(key_instance):
    url = f'http://34.118.233.244:80/news/{key_instance}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return 'ERROR', response.status_code

def more_frequent_word(key_instance):
    url = f'http://34.118.233.244:80/get_more_frequent_word/{key_instance}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return 'ERROR', response.status_code

def get_news_frequency(key_instance):
    url = f'http://34.118.233.244:80/get_news_frequency/{key_instance}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return 'ERROR', response.status_code

def most_frequenttime(key_instance):
    url = f'http://34.118.233.244:80/most_frequent_time/{key_instance}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return 'ERROR', response.status_code

@login_required
@superuser_required
def detail(request, drop_id):
    drop = Drops.objects.get(id=drop_id, user=request.user)
    data = Drops.objects.filter(user=request.user)

    most_frequent_time = most_frequenttime(drop.key_instance)
    news = news_by_key(drop.key_instance)
    bar_data = more_frequent_word(drop.key_instance)
    news_frequency = get_news_frequency(drop.key_instance)

    context={
        "news":news,
        "data":data,
        "drop":drop,
        "bar_data":bar_data,
        "news_frequency":news_frequency,
        "most_frequent_time":most_frequent_time,
    }

    return render(request,"drops/detail.html",context)