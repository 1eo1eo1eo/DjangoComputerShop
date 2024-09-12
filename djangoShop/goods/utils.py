from django.db.models import Q

from .models import Product


def query_search(query):

    if query.isdigit() and len(query) <= 5:
        return Product.objects.filter(id=int(query))
