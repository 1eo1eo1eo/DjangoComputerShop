from django import template

from basket.models import Basket
from basket.utils import get_user_baskets


register = template.Library()


@register.simple_tag
def user_baskets(request):
    return get_user_baskets(request)
