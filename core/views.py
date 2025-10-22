from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout

from core.forms import RegisterForm

# Create your views here.


def home(request):
    return render(request, "core/home.html", {"posts": "posts"})


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})
