from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout

from core.forms import RegisterForm

from django.shortcuts import render, redirect
from .forms import RegisterCandidateForm, RegisterForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Post

# Create your views here.


@login_required(login_url="/login")
def home(request):
    return render(request, "core/home.html", {"posts": "posts"})


def sign_up(request):
    if request.method == "POST":
        form = RegisterCandidateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterCandidateForm()

    return render(request, "registration/sign_up.html", {"form": form})


@login_required(login_url="/login")
@permission_required("core.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, "core/create_post.html", {"form": form})
