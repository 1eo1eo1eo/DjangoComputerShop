from django.template.loader import render_to_string
from django.urls import reverse

from basket.models import Basket
from basket.utils import get_user_baskets


class BasketMixin:
    def get_basket(self, request, product=None, basket_id=None):
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        if product:
            query_kwargs["product"] = product

        if basket_id:
            query_kwargs["id"] = basket_id

        return Basket.objects.filter(**query_kwargs).first()

    def render_basket(self, request):
        user_baskets = get_user_baskets(request)
        context = {
            "baskets": user_baskets,
        }

        referer = request.META.get("HTTP_REFERER")
        if reverse("orders:create_order") in referer:
            context["order"] = True

        return render_to_string(
            "includes/included_basket.html",
            context,
            request=request,
        )
