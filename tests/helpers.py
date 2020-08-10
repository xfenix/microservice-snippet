"""Full view tests."""
from fastapi.testclient import TestClient

from snippet_service import settings
from snippet_service.__main__ import APP_OBJ


def build_test_client() -> TestClient:
    """Build test app helper."""
    return TestClient(APP_OBJ)


def build_url_for_service(core_url: str) -> str:
    """Url builder."""
    return settings.API_PREFIX + core_url
