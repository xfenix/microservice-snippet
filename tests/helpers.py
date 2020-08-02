"""Full view tests.
"""
from fastapi.testclient import TestClient

from snippet_service.__main__ import APP_OBJ


def build_test_client():
    """
    """
    return TestClient(APP_OBJ)
