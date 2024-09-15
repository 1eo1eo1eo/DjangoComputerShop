from typing import TYPE_CHECKING

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import auth

from users.forms import UserLoginForm

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


def login(request: "HttpRequest") -> "HttpResponse":

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("main:home"))
    else:
        form = UserLoginForm()

    context: dict = {
        "title": "BYD - Authorization",
        "form": form,
    }

    return render(request, "users/login.html", context)


def registration(request: "HttpRequest") -> "HttpResponse":
    context: dict = {
        "title": "BYD - Registration",
    }

    return render(request, "users/registration.html", context)


def profile(request: "HttpRequest") -> "HttpResponse":
    context: dict = {
        "title": "BYD - Profile",
    }

    return render(request, "users/profile.html", context)


def logout(request: "HttpRequest") -> "HttpResponse":
    context: dict = {
        "title": "BYD - Logout",
    }

    return render(request, "users/login.html", context)
