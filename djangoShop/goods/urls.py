from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("product/", views.product, name="product"),
]
