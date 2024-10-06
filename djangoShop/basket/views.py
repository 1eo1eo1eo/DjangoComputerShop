from django.http import JsonResponse
from django.views import View

from basket.models import Basket
from goods.models import Product
from basket.mixins import BasketMixin


class BasketAddView(BasketMixin, View):

    def post(self, request):
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)

        basket = self.get_basket(request, product=product)

        if basket:
            basket.quantity += 1
            basket.save()
        else:
            Basket.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=(
                    request.session.session_key
                    if not request.user.is_authenticated
                    else None
                ),
                product=product,
                quantity=1,
            )

        response_data = {
            "message": "Product added to the basket",
            "cart_items_html": self.render_basket(request),
        }

        return JsonResponse(response_data)


class BasketChangeView(BasketMixin, View):

    def post(self, request):
        basket_id = request.POST.get("cart_id")
        quantity = request.POST.get("quantity")
        basket = self.get_basket(request, basket_id=basket_id)

        basket.quantity = quantity
        basket.save()

        response_data = {
            "message": "Quantity changed",
            "cart_items_html": self.render_basket(request),
            "quantity": quantity,
        }

        return JsonResponse(response_data)


class BasketRemoveView(BasketMixin, View):

    def post(self, request):
        basket_id = request.POST.get("cart_id")
        basket = self.get_basket(request, basket_id=basket_id)
        quantity = basket.quantity

        basket.delete()

        response_data = {
            "message": "Product deleted",
            "cart_items_html": self.render_basket(request),
            "quantity_deleted": quantity,
        }

        return JsonResponse(response_data)
