import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse("main:home")
    response = client.get(url)

    assert response.status_code == 200
    assert "BYD - Home Page" in response.content.decode()
    assert "BYD PC Store" in response.content.decode()
