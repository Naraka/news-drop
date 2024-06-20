from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="drops"),
    path('delete_drop/<int:drop_id>', views.delete_drop , name="delete_drop"),
    path('detail/<int:drop_id>', views.detail , name="detail"),
]
