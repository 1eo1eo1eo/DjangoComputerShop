from django.contrib import admin

from goods.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields: dict[str, tuple] = {"slug": ("name",)}
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields: dict[str, tuple] = {"slug": ("name",)}
    list_display = ("id", "name")
    list_display_links = ("id", "name")
