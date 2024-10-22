import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_profile_view_get_authenticated(client, create_test_user):  # noqa: ARG001
    creds = {
        "username": "testuser",
        "password": "testpassword",
    }

    client.login(
        username=creds["username"],
        password=creds["password"],
    )

    url = reverse("users:profile")
    response = client.get(url)

    assert response.status_code == 200
    assert "BYD - Profile" in response.content.decode()


@pytest.mark.django_db
def test_profile_view_get_unauthenticated(client):
    url = reverse("users:profile")
    response = client.get(url)

    assert response.status_code == 302
