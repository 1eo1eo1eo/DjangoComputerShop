from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from .models import Product


def catalog(request, category_slug, page=1):

    if category_slug == "all-products":
        queryset = Product.objects.order_by("id")
    else:
        queryset = get_list_or_404(Product.objects.filter(category__slug=category_slug))

    paginator = Paginator(queryset, 3)
    current_page = paginator.page(page)

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
