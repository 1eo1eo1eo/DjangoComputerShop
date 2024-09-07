from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("product/<int:product_id>/", views.product, name="product"),
]
