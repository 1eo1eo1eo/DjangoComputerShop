from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import auth, messages

from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

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
                messages.success(
                    request,
                    f"{user.first_name}, you signed in",
                )
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
            messages.success(
                request,
                f"{user.first_name}, you successfully registered and signed in!",
            )
            return HttpResponseRedirect(reverse("users:login"))
    else:
        form = UserRegistrationForm()

    context: dict = {
        "title": "BYD - Registration",
        "form": form,
    }

    return render(request, "users/registration.html", context)


@login_required
def profile(request: "HttpRequest") -> "HttpResponse":
    if request.method == "POST":
        form = UserProfileForm(
            data=request.POST,
            instance=request.user,
            files=request.FILES,
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Profile successfully updated!",
            )
            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = UserProfileForm(instance=request.user)

    context: dict = {
        "title": "BYD - Profile",
        "form": form,
    }

    return render(request, "users/profile.html", context)


def logout(request: "HttpRequest") -> "HttpResponse":
    messages.warning(
        request,
        "You logged out!",
    )
    auth.logout(request)
    return redirect(reverse("main:home"))
