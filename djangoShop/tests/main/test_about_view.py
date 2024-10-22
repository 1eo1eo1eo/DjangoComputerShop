import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse("main:about")
    response = client.get(url)

    assert response.status_code == 200
    assert "BYD - About us" in response.content.decode()
    assert "About us" in response.content.decode()
    assert "Some text about our company" in response.content.decode()
