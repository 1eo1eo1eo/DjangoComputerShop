import pytest

from goods.models import Product, Category


@pytest.fixture
def create_test_user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        password="testpassword",
    )


### Goods


@pytest.fixture
def setUpTestData():
    category = Category.objects.create(
        name="GPUs",
        slug="gpus",
    )
    category_all = Category.objects.create(
        name="All products",
        slug="all-products",
    )

    for i in range(5):
        Product.objects.create(
            name=f"Product {i}",
            slug=f"product-{i}",
            category=category,
            price=100 + i,
            discount=i if i % 2 == 0 else 0,
        )

    for i in range(5):
        Product.objects.create(
            name=f"Good {i}",
            slug=f"good-{i}",
            category=category,
            price=100 + i,
            discount=i if i % 2 == 0 else 0,
        )

    return category, category_all
