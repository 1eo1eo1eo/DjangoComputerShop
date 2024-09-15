from typing import TYPE_CHECKING

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import auth

from users.forms import UserLoginForm, UserRegistrationForm

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

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse("users:login"))
    else:
        form = UserRegistrationForm()

    context: dict = {
        "title": "BYD - Registration",
        "form": form,
    }

    return render(request, "users/registration.html", context)


def profile(request: "HttpRequest") -> "HttpResponse":
    context: dict = {
        "title": "BYD - Profile",
    }

    return render(request, "users/profile.html", context)


def logout(request: "HttpRequest") -> "HttpResponse":
    auth.logout(request)
    return redirect(reverse("main:home"))
