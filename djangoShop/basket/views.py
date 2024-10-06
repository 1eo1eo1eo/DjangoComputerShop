from django.http import JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.views import View

from basket.models import Basket
from basket.templatetags.baskets_tags import user_baskets
from basket.utils import get_user_baskets
from goods.models import Product
from basket.mixins import BasketMixin


class BasketAddView(BasketMixin, View):

    def post(self, request):
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)

        basket = self.get_basket(request, product=product)

        if basket:
            basket.quantity += 1
            basket.save()
        else:
            Basket.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=(
                    request.session.session_key
                    if not request.user.is_authenticated
                    else None
                ),
                product=product,
                quantity=1,
            )

        response_data = {
            "message": "Product added to the basket",
            "cart_items_html": self.render_basket(request),
        }

        return JsonResponse(response_data)


class BasketChangeView(BasketMixin, View):

    def post(self, request):
        basket_id = request.POST.get("cart_id")
        quantity = request.POST.get("quantity")
        basket = self.get_basket(request, basket_id=basket_id)

        basket.quantity = quantity
        basket.save()

        response_data = {
            "message": "Quantity changed",
            "cart_items_html": self.render_basket(request),
            "quantity": quantity,
        }

        return JsonResponse(response_data)


def basket_remove(
    request,
):

    basket_id = request.POST.get("cart_id")

    basket = Basket.objects.get(id=basket_id)
    quantity = basket.quantity
    basket.delete()

    user_baskets = get_user_baskets(request)

    context = {
        "baskets": user_baskets,
    }

    referer = request.META.get("HTTP_REFERER")
    if reverse("orders:create_order") in referer:
        context["order"] = True

    basket_items_html = render_to_string(
        "includes/included_basket.html",
        context,
        request=request,
    )

    response_data = {
        "message": "Товар удален",
        "cart_items_html": basket_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)
