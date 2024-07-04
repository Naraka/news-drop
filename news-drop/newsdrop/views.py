from django.shortcuts import render
from drops.models import Drops
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def superuser_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap


@login_required
@superuser_required
def index(request):
    if request.method == "GET":
        drops = Drops.objects.filter(user=request.user)
        return render(request, "index.html", {
            "data": drops,
        })

def server_error_view(request):
    return redirect('drops')
