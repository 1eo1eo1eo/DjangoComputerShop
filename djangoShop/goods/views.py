from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from .utils import query_search

from .models import Product


def catalog(request, category_slug=None):

    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)
    query = request.GET.get("q", None)

    if category_slug == "all-products":
        queryset = Product.objects.order_by("id")
    elif query:
        queryset = query_search(query)
    else:
        queryset = get_list_or_404(Product.objects.filter(category__slug=category_slug))

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


def product(request, product_slug):

    product = Product.objects.get(slug=product_slug)

    context = {
        "product": product,
    }

    return render(request, "goods/product.html", context=context)
