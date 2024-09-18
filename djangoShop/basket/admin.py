from django.contrib import admin

from basket.models import Basket


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass
