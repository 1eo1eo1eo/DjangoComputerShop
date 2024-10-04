from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("search/", views.CatalogView.as_view(), name="search"),
    path("<slug:category_slug>/", views.CatalogView.as_view(), name="catalog"),
    path("product/<slug:product_slug>/", views.ProductView.as_view(), name="product"),
]
