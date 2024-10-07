from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.views.generic import CreateView, UpdateView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.core.cache import cache

from basket.models import Basket
from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


class LoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("main:home")

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse_lazy("users:logout"):
            return redirect_page
        return reverse_lazy("main:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "BYD - Authentication"
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)

            if session_key:
                old_baskets = Basket.objects.filter(user=user)

                if old_baskets.exists():
                    old_baskets.delete()

                Basket.objects.filter(session_key=session_key).update(user=user)

                messages.success(
                    self.request,
                    f"{user.username}, you signed in",
                )

                return HttpResponseRedirect(self.get_success_url())


class RegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "BYD - Registration"
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Basket.objects.filter(session_key=session_key).update(user=user)

        messages.success(
            self.request,
            f"{user.username}, registration successfully completed and you signed in",
        )

        return HttpResponseRedirect(self.success_url)


class ProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile successfully updated")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "BYD - Profile"

        orders = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )
        context["orders"] = self.set_get_cache(
            orders,
            f"user_orders_{self.request.user.id}",
            60,
        )

        return context


class BasketView(TemplateView):
    template_name = "users/basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "BYD - Basket"
        return context


@login_required
def logout(request: "HttpRequest") -> "HttpResponse":
    messages.warning(
        request,
        "You logged out!",
    )
    auth.logout(request)
    return redirect(reverse("main:home"))
