from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import auth, messages
from django.db.models import Prefetch

from basket.models import Basket
from orders.models import Order, OrderItem
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

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(
                    request,
                    f"{user.first_name}, you signed in",
                )

                if session_key:
                    Basket.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get("next", None)
                if redirect_page and redirect_page != reverse("users:logout"):
                    return HttpResponseRedirect(request.POST.get("next"))

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

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)
            messages.success(
                request,
                f"{user.first_name}, you successfully registered and signed in!",
            )

            if session_key:
                Basket.objects.filter(session_key=session_key).update(user=user)

            return HttpResponseRedirect(reverse("users:profile"))
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

    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        )
        .order_by("-id")
    )

    context: dict = {
        "title": "BYD - Profile",
        "form": form,
        "orders": orders,
    }

    return render(request, "users/profile.html", context)


def basket(request: "HttpRequest") -> "HttpResponse":
    return render(request, "users/basket.html")


@login_required
def logout(request: "HttpRequest") -> "HttpResponse":
    messages.warning(
        request,
        "You logged out!",
    )
    auth.logout(request)
    return redirect(reverse("main:home"))
