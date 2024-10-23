import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse("users:login")
    response = client.get(url)

    assert response.status_code == 200
    assert "BYD - Authentication" in response.content.decode()


@pytest.mark.django_db
def test_login_view_post_success(client, create_test_user):  # noqa: ARG001

    creds = {
        "username": "testuser",
        "password": "testpassword",
    }

    url = reverse("users:login")
    response = client.post(
        url,
        {
            "username": creds["username"],
            "password": creds["password"],
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("main:home")


@pytest.mark.django_db
def test_login_views_post_fail(client):
    wrong_creds = {
        "username": "wrongtestuser",
        "password": "wrongtestpassword",
    }

    url = reverse("users:login")
    response = client.post(
        url,
        {
            "username": wrong_creds["username"],
            "password": wrong_creds["password"],
        },
    )

    assert response.status_code == 200
    assert (
        "Пожалуйста, введите правильные имя пользователя и пароль."
        in response.content.decode()
    )
