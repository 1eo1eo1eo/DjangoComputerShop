import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_logout(client, create_test_user):  # noqa: ARG001
    client.login(
        username="testuser",
        password="testpassword",
    )
    url = reverse("users:logout")
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("main:home")
