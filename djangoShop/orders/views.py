from typing import TYPE_CHECKING

from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.db import transaction
from django.contrib import messages

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from basket.models import Basket

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


def create_order(request: "HttpRequest") -> "HttpResponse":

    if request.method == "POST":
        form = CreateOrderForm(data=request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    basket_items = Basket.objects.filter(user=user)

                    if basket_items.exists():
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data["phone_number"],
                            requires_delivery=form.cleaned_data["requires_delivery"],
                            delivery_address=form.cleaned_data["delivery_address"],
                            payment_on_get=form.cleaned_data["payment_on_get"],
                        )

                        for basket_item in basket_items:
                            product = basket_item.product
                            name = basket_item.product.name
                            price = basket_item.product.sell_price()
                            quantity = basket_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(
                                    f"Недостаточное количество товара {name} на складе\
                                                      В наличии - {product.quantity}"
                                )

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()

                        basket_items.delete()

                        messages.success(request, "Заказ оформлен")
                        return redirect("users:profile")

            except ValidationError as e:
                messages.success(request, str(e))
                return redirect("orders:create_order")

    else:
        initial = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }

        form = CreateOrderForm(initial=initial)

    context = {
        "title": "BYD - Оформление заказа",
        "form": form,
    }

    return render(
        request,
        "orders/create_order.html",
        context=context,
    )
