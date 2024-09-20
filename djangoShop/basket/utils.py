from basket.models import Basket


def get_user_baskets(request):
    if request.user.is_authenticated:
        return Basket.objects.filter(user=request.user)
