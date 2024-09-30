from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


def create_order(request: "HttpRequest") -> "HttpResponse":
    return render(request, "orders/create_order.html")
