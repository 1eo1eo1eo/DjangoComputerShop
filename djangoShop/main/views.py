from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def index(request: "HttpRequest") -> "HttpResponse":
    context: dict = {
        "title": "DPC - Home Page",
        "content": "Магазин компьютеров BYD",
    }

    return render(request, "main/index.html", context)


def about(request: "HttpRequest") -> "HttpResponse":
    context: dict = {
        "title": "DPC - About us",
        "content": "About us",
        "text_on_page": "Some text about our company",
    }

    return render(request, "main/about.html", context)
