from django.core.exceptions import PermissionDenied

BASE_URL = "http://34.118.239.153:80"
# BASE_URL = "http://127.0.0.1:80"

def superuser_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap