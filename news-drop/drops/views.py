from django.shortcuts import render, redirect
import requests
from .forms import DropForm
from django.contrib.auth.decorators import login_required

def post_bot(key_instance):
    url = 'http://127.0.0.1:80/post_bot/'
    data = {"key_instance": key_instance}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.text
    else:
        return response.status_code


def index(request):
    if request.method == "GET":
        url = "http://127.0.0.1:80/get_bots/"
        response = requests.get(url=url)

        if response.status_code == 200:
            data = response.json()
        else:
            data = {"error":response.status_code}

        return render(request,"drops/index.html",{
            "data":data,
            "form":DropForm
        })
    else:
        try:
            try:
                post_bot(request.POST["key_instance"])
            except:
                pass
            bot = DropForm(request.POST)
            newbot = bot.save(commit=False)
            newbot.user = request.user
            newbot.save()
            return redirect("drops")
        except:
            pass

