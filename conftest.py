import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def api_client() -> APIClient:
    """
    Providing an instance of Django REST framework's `APIClient`.

    Returns:
        an instance of `APIClient`
    """
    return APIClient()