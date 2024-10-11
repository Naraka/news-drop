from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import handler500
from .views import server_error_view, health_check

handler500 = server_error_view

urlpatterns = [
    path('', views.index , name="index"),
    path('healthz/', health_check),
    path('admin/', admin.site.urls),
]
