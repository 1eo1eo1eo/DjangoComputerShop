from typing import TYPE_CHECKING

from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from basket.models import Basket

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy("users:profile")

    def get_initial(self):
        initial = super().get_initial()
        initial["first_name"] = self.request.user.first_name
        initial["last_name"] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
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
                                f"Insufficient quantity of goods {name} in the warehouse\
                                                    In stock - {product.quantity}"
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

                    messages.success(self.request, "The order has been placed")
                    return redirect("users:profile")

        except ValidationError as e:
            messages.success(self.request, str(e))
            return redirect("orders:create_order")

    def form_invalid(self, form):
        messages.error(self.request, "The order was not placed")
        return redirect("orders:create_order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "BYD - Making an order"
        context["order"] = True
        return context
