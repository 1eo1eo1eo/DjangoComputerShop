from django.db.models.base import Model as Model
from django.http import Http404
from django.views.generic import DetailView, ListView

from goods.utils import query_search

from goods.models import Product


class CatalogView(ListView):
    model = Product
    template_name: str = "goods/catalog.html"
    context_object_name: str = "goods"
    paginate_by: int = 3
    allow_empty: bool = False

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")

        if category_slug == "all-products":
            queryset = super().get_queryset().order_by("-id")
        elif query:
            queryset = query_search(query)
        else:
            queryset = super().get_queryset().filter(category__slug=category_slug)

            if not queryset.exists():
                raise Http404()

        if on_sale:
            queryset = queryset.filter(discount__gt=0)

        if order_by and order_by != "default":
            queryset = queryset.order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "BYD - Catalog"
        context["slug_url"] = self.kwargs.get("category_slug")
        return context


class ProductView(DetailView):

    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self, queryset=None) -> Product:
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context
