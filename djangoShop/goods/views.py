from django.shortcuts import render
from .models import Product


def catalog(request):

    queryset = Product.objects.order_by("id")
    context: dict = {
        "title": "BYD - Catalog",
        "goods": queryset,
    }
    return render(request, "goods/catalog.html", context)


def product(request):
    return render(request, "goods/product.html")
