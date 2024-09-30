from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("create-order/", views.create_order, name="create_order"),
]
