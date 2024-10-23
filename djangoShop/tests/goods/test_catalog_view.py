import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_pagination_is_correct(client, setUpTestData):
    category, category_all = setUpTestData

    response = client.get(
        reverse(
            "catalog:catalog",
            kwargs={"category_slug": category.slug},
        )
    )

    assert response.status_code == 200
    assert "goods" in response.context
    assert len(response.context["goods"]) == 3

    response = client.get(
        reverse(
            "catalog:catalog",
            kwargs={"category_slug": category.slug},
        )
        + "?page=2"
    )

    assert response.status_code == 200
    assert len(response.context["goods"]) == 3


@pytest.mark.django_db
def test_search_functionality(client, setUpTestData):  # noqa: ARG001
    search_query = "Product"
    response = client.get(
        reverse("catalog:search") + f"?q={search_query}",
    )

    assert response.status_code == 200

    assert "goods" in response.context
    products = response.context["goods"]

    assert len(products) == 3
    assert products[0].name == "Product 4"

    response = client.get(
        reverse("catalog:search") + f"?q={search_query}&page=2",
    )

    assert len(response.context["goods"]) == 2


@pytest.mark.django_db
def test_on_sale_filter(client, setUpTestData):  # noqa: ARG001
    response = client.get(
        reverse(
            "catalog:catalog",
            kwargs={"category_slug": "gpus"},
        )
        + "?on_sale=on"
        + "&order_by=default"
    )

    assert response.status_code == 200
    assert len(response.context["goods"]) == 3

    response = client.get(
        reverse(
            "catalog:catalog",
            kwargs={"category_slug": "gpus"},
        )
        + "?on_sale=on"
        + "&order_by=default"
        + "&page=2"
    )

    assert response.status_code == 200
    assert len(response.context["goods"]) == 1
