from django.contrib import admin

from basket.models import Basket


class CarTabAdmin(admin.TabularInline):
    model = Basket
    fields = (
        "product",
        "quantity",
        "created_timestamp",
    )
    search_fields = (
        "product",
        "quantity",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 1


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "product__name",
        "quantity",
        "created_timestamp",
    ]
    list_filter = [
        "created_timestamp",
        "user",
        "product__name",
    ]
