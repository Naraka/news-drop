from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "GET":
            context = {
                "form":UserCreationForm
            }
            return render(request, "users/signup.html",context)
        else:
            if request.POST["password1"] == request.POST["password2"]:
                try:
                    user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                    user.save()
                    login(request, user)
                    return redirect("/")
                except:
                    context = {
                        "form":UserCreationForm,
                        "error":"User already exists"
                    }
                    return render(request, "users/signup.html",context)
            else:
                context = {
                    "form":UserCreationForm,
                    "error":"confirmation password do not match"
                }
                return render(request, "users/signup.html",context)


def signout(request):
    logout(request)
    return redirect("/signin")

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "GET":
            context = {
                "form": AuthenticationForm
            }
            return render(request, "users/signin.html", context)
        else:
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user is None:
                context = {
                    "form": AuthenticationForm,
                    "error": "error in sign in user is none"
                    }
                return render(request, "users/signin.html", context)
            else:
                next_url = request.POST.get('next')
                login(request, user)
                try:
                    return redirect(next_url)
                except:
                    return redirect("/")
