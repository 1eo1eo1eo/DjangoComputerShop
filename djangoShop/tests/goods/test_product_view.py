import pytest
from django.urls import reverse
from decimal import Decimal


@pytest.mark.django_db
def test_product_view(client, setUpTestData):
    category, category_all = setUpTestData

    response = client.get(
        reverse("catalog:product", kwargs={"product_slug": "product-1"})
    )
    assert response.status_code == 200
    assert response.context["product"].name == "Product 1"
    assert response.context["product"].price == Decimal("101.00")
    assert response.context["product"].discount == Decimal("0.00")
    assert "Product 1" in response.content.decode()
