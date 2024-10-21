import json
from unittest.mock import patch
import pytest
from django.urls import reverse
from users.models import User


@pytest.mark.django_db
def test_registration_view_get(client):
    url = reverse("users:registration")
    response = client.get(url)

    assert response.status_code == 200
    assert "BYD - Registration" in response.content.decode()


@pytest.mark.django_db
@patch("users.views.produce")
def test_registration_view_post_success(mock_produce, client):
    url = reverse("users:registration")

    data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "Username",
        "email": "test@test.test",
        "password1": "qweqwe123123",
        "password2": "qweqwe123123",
    }

    response = client.post(
        url,
        data,
    )

    assert response.status_code == 302
    assert User.objects.filter(email="test@test.test").exists()

    mock_produce.assert_called_once_with(
        json.dumps(
            {
                "email": "test@test.test",
                "password": User.objects.get(email="test@test.test").password,
            }
        )
    )


@pytest.mark.django_db
def test_registration_view_post_failed(client):
    url = reverse("users:registration")

    data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "Username",
        "email": "test@test.test",
        "password1": "qweqwe123123",
        "password2": "321321ewqewq",
    }

    response = client.post(
        url,
        data,
    )

    assert response.status_code == 200
    assert "Введенные пароли не совпадают." in response.content.decode()
