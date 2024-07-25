from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import ImageUserform
from .models import ImageUser


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
@login_required
def profile(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        imageformuser = ImageUserform()
        iamgeuser = ImageUser.objects.filter(user=request.user)

    context = {
        "user": request.user,
        "imageformuser": imageformuser,
        "iamgeuser": iamgeuser

    }
    return render(request, 'users/profile.html', context=context)


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUserform(request.POST, request.FILES)
        if form.is_valid():
            newimage = form.save(commit=False)
            newimage.user = request.user
            newimage.save()
            messages.success(request, 'Image uploaded successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        return redirect("/")