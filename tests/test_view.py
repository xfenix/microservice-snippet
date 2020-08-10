"""Full view tests."""
from unittest import mock

import pytest
from fastapi.testclient import TestClient

from tests import helpers


MAIN_URL: str = helpers.build_url_for_service("/")


def test_get_stupid_without_params():
    """Basic stupid test."""
    assert helpers.build_test_client().get(MAIN_URL).status_code == 422


@pytest.mark.parametrize("case_url", ("https://yandex.ru/", "https://habr.com/", "https://lenta.ru"))
def test_get_good(monkeypatch, case_url: str):
    """Main test scenario."""
    monkeypatch.setattr("aiohttp.ClientSession", mock.MagicMock())
    assert helpers.build_test_client().get(MAIN_URL + "?source_url=" + case_url).status_code == 422
