import pytest


@pytest.fixture
def create_test_user(db, django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        password="testpassword",
    )
