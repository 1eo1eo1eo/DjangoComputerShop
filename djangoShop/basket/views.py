from django.http import JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string

from basket.models import Basket
from basket.templatetags.baskets_tags import user_baskets
from basket.utils import get_user_baskets
from goods.models import Product


def basket_add(
    request,
):

    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user, product=product)

        if baskets.exists():
            basket = baskets.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            Basket.objects.create(user=request.user, product=product, quantity=1)

    else:
        baskets = Basket.objects.filter(
            session_key=request.session.session_key,
            product=product,
        )

        if baskets.exists():
            basket = baskets.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            Basket.objects.create(
                session_key=request.session.session_key,
                product=product,
                quantity=1,
            )

    user_baskets = get_user_baskets(request)
    basket_items_html = render_to_string(
        "includes/included_basket.html",
        {"baskets": user_baskets},
        request=request,
    )

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": basket_items_html,
    }

    return JsonResponse(response_data)


def basket_change(
    request,
):

    basket_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    basket = Basket.objects.get(id=basket_id)

    basket.quantity = quantity
    basket.save()

    user_baskets = get_user_baskets(request)

    context = {
        "baskets": user_baskets,
    }

    referer = request.META.get("HTTP_REFERER")
    if reverse("orders:create_order") in referer:
        context["order"] = True

    cart_items_html = render_to_string(
        "includes/included_basket.html",
        context,
        request=request,
    )

    response_data = {
        "message": "Quantity changed",
        "cart_items_html": cart_items_html,
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
