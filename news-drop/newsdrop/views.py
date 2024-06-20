from django.shortcuts import render
from drops.models import Drops


def index(request):
    if request.method == "GET":
        drops = Drops.objects.filter(user=request.user)
        return render(request, "index.html", {
            "data": drops,
        })
