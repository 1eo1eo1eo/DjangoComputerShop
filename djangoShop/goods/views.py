from typing import TYPE_CHECKING

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import Http404

from .utils import query_search

from .models import Product

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


def catalog(request: "HttpRequest", category_slug=None) -> "HttpResponse":

    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)
    query = request.GET.get("q", None)

    if category_slug == "all-products":
        queryset = Product.objects.order_by("id")
    elif query:
        queryset = query_search(query)
    else:
        queryset = Product.objects.filter(category__slug=category_slug)

        if not queryset.exists():
            raise Http404()

    if on_sale:
        queryset = queryset.filter(discount__gt=0)

    if order_by and order_by != "default":
        queryset = queryset.order_by(order_by)

    paginator = Paginator(queryset, 3)
    current_page = paginator.page(int(page))

    context: dict = {
        "title": "BYD - Catalog",
        "goods": current_page,
        "slug_url": category_slug,
    }
    return render(request, "goods/catalog.html", context)


def product(request: "HttpRequest", product_slug) -> "HttpResponse":

    product = Product.objects.get(slug=product_slug)

    context: dict = {
        "product": product,
    }

    return render(request, "goods/product.html", context=context)
