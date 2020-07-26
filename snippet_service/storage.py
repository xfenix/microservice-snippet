"""Parser interfaces and realisations.
"""
from __future__ import annotations
import typing


@typing.runtime_checkable
class GeneralInterface(typing.Protocol):
    """Interface contract.
    """

    def exists(self) -> bool:
        """Check is snippet already in storage.
        """
        ...

    def save(self, snippet_data: dict) -> None:
        """Save snippet data in storage.
        """
        ...

    def fetch(self) -> dict:
        """Fetch snippet data from storage.
        """
        ...


class BasicStorage:
    """Very simple parent.
    """

    def __init__(self, source_url: str) -> None:
        self._data_url: str = source_url


class NoStorage(BasicStorage):
    """No storage backend.
    """

    def __init__(self, source_url: str) -> None:
        self._data_url: str = source_url

    def exists(self) -> bool:
        """Check is snippet already in storage.
        """
        return False

    def save(self, snippet_data: dict) -> None:
        """Save snippet data in storage.
        """
        return

    def fetch(self) -> dict:
        """Fetch snippet data from storage.
        """
        return {}
