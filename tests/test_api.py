from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from scrapenfill.rest.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_convert_rejects_missing_file(client):
    response = client.post("/convert/")
    assert response.status_code == 422


def test_convert_rejects_empty_filename(client):
    response = client.post(
        "/convert/",
        files={"source": ("", BytesIO(b"test"), "text/plain")},
    )
    assert response.status_code == 422


def test_health_check_no_get_on_convert(client):
    response = client.get("/convert/")
    assert response.status_code == 405
