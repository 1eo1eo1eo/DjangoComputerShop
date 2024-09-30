from tabnanny import verbose
from django.db import models
from django.forms import CharField

from goods.models import Product
from users.models import User


class OrderItemQuerySet(models.QuerySet):

    def total_price(self):
        return sum(product.products_price() for product in self)

    def total_quantity(self):
        if self:
            return sum(product.quantity for product in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name="Пользователь",
        on_delete=models.SET_DEFAULT,
        default=None,
        blank=True,
        null=True,
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заказа",
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
    )
    requires_delivery = models.BooleanField(
        default=False,
        verbose_name="Требуется доставка",
    )
    delivery_address = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Адрес доставки",
    )
    payment_on_get = models.BooleanField(
        default=False,
        verbose_name="Оплата при получении",
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name="Оплачено",
    )
    status = models.CharField(
        max_length=50,
        default="В обработке",
        verbose_name="Статус заказа",
    )

    class Meta:
        db_table: str = "Order"
        verbose_name: str = "Order"
        verbose_name_plural: str = "Orders"

    def __str__(self) -> str:
        return f"Order № {self.pk} | Customer {self.user.first_name} {self.user.last_name} "


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        verbose_name="Заказ",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to=Product,
        verbose_name="Товар",
        on_delete=models.CASCADE,
        default=None,
        null=True,
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название",
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Цена",
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество",
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата продажи",
    )

    class Meta:
        db_table: str = "Order item"
        verbose_name: str = "Sold product"
        verbose_name_plural: str = "Sold products"

    objects = OrderItemQuerySet.as_manager()

    def products_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self) -> str:
        return f"Product {self.name} | Order № {self.order.pk}"
