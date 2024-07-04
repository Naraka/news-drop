from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import handler500
from .views import server_error_view

handler500 = server_error_view

urlpatterns = [
    path('', views.index , name="index"),
    path('admin/', admin.site.urls),
    path('drops/', include("drops.urls")),
    path('', include("users.urls")),
]
