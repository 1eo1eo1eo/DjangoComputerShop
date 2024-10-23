import pytest
from django.urls import reverse

from basket.models import Basket
from goods.models import Product


@pytest.mark.django_db
def test_basket_change_auth_user(
    client,
    create_test_user,
    setUpTestData,
):
    client.login(username="testuser", password="testpassword")

    client.get(reverse("users:login"))

    product = Product.objects.get(slug="product-1")

    basket = Basket.objects.create(
        user=create_test_user,
        product=product,
        quantity=1,
    )

    response = client.post(
        reverse("basket:basket_change"),
        {
            "cart_id": basket.id,
            "quantity": 2,
            "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        },
        HTTP_REFERER=reverse(
            "catalog:catalog", kwargs={"category_slug": "all-products"}
        ),
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Quantity changed"

    basket.refresh_from_db()
    assert basket.quantity == 2
