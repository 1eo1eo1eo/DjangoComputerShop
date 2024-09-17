from django.urls import path

from . import views


app_name = "basket"

urlpatterns = [
    path("basket-add/<int:product_id>/", views.basket_add, name="basket_add"),
    path("basket-change/<int:product_id>/", views.basket_change, name="basket_change"),
    path("basket-remove/<int:product_id>/", views.basket_remove, name="basket_remove"),
]
