import pytest
from django.urls import reverse

from basket.models import Basket
from goods.models import Product


@pytest.mark.django_db
def test_basket_add_auth_user(
    client,
    create_test_user,
    setUpTestData,
):
    client.login(username="testuser", password="testpassword")

    client.get(reverse("users:login"))

    response = client.post(
        reverse("basket:basket_add"),
        {
            "product_id": 1,
            "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        },
        HTTP_REFERER=reverse(
            "catalog:catalog", kwargs={"category_slug": "all-products"}
        ),
    )
    product = Product.objects.get(id=1)

    assert response.status_code == 200
    assert response.json()["message"] == "Product added to the basket"

    basket = Basket.objects.filter(
        user=create_test_user,
        product=product,
    ).first()

    assert basket is not None
    assert basket.quantity == 1
