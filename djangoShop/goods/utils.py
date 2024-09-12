from django.db.models import Q

from .models import Product


def query_search(query):

    if query.isdigit() and len(query) <= 5:
        return Product.objects.filter(id=int(query))

    keywords = [word for word in query.split() if len(word) > 2]

    q_objects = Q()

    for token in keywords:
        q_objects |= Q(name__icontains=token)

    return Product.objects.filter(q_objects)
