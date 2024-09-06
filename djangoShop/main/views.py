from typing import TYPE_CHECKING

from django.shortcuts import render

from goods.models import Category

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home(request: "HttpRequest") -> "HttpResponse":

    category = Category.objects.all()

    context: dict = {
        "title": "BYD - Home Page",
        "content": "BYD PC Store",
        "categories": category,
    }

    return render(request, "main/index.html", context)


def about(request: "HttpRequest") -> "HttpResponse":
    context: dict = {
        "title": "DPC - About us",
        "content": "About us",
        "text_on_page": "Some text about our company",
    }

    return render(request, "main/about.html", context)
