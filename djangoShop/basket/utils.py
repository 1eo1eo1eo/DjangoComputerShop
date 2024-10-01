from basket.models import Basket


def get_user_baskets(request):
    if request.user.is_authenticated:
        return Basket.objects.filter(
            user=request.user,
        ).select_related("product")

    if not request.session.session_key:
        request.session.create()

    return Basket.objects.filter(
        session_key=request.session.session_key,
    ).select_related("product")
