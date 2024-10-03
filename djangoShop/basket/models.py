from django.db import models

from goods.models import Product
from users.models import User


class BasketQuerySet(models.QuerySet):

    def total_price(self):
        return sum(basket.products_price() for basket in self)

    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Basket(models.Model):

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="User",
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        verbose_name="Product",
    )
    quantity = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Quantity",
    )
    session_key = models.CharField(
        max_length=32,
        blank=True,
        null=True,
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Add time",
    )

    class Meta:
        db_table = "basket"
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"
        ordering = ["id"]

    objects = BasketQuerySet().as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self) -> str:
        if self.user:
            return f"Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}"

        return f"Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}"
