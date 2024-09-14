from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


def login(request: "HttpRequest") -> "HttpResponse":
    context: dict = {
        "title": "BYD - Authorization",
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
