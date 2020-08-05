"""Full view tests.
"""
from fastapi.testclient import TestClient

from tests import helpers


def test_with_empty_params():
    """Basic validation test.
    """
    assert helpers.build_test_client().get("/").status_code == 422
