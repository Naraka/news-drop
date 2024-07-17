from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup , name="signup"),
    path('signout/', views.signout , name="signout"),
    path('signin/', views.signin , name="signin"),
    path('profile/', views.profile , name="profile"),
    path('upload_image/', views.upload_image , name="upload_image"),
]
