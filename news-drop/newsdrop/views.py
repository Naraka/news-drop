from django.shortcuts import render
from drops.models import Drops
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.method == "GET":
        drops = Drops.objects.filter(user=request.user)
        return render(request, "index.html", {
            "data": drops,
        })
