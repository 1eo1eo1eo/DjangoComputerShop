from django.contrib import admin

from basket.admin import BasketTabularAdmin
from orders.admin import OrderTabularAdmin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]
    inlines = [
        BasketTabularAdmin,
        OrderTabularAdmin,
    ]
