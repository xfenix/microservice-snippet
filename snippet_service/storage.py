"""Parser interfaces and realisations.
"""
from __future__ import annotations
import typing


@typing.runtime_checkable
class BasicStorage(typing.Protocol):
    def __init__(self, source_url: str) -> None:
        self._data_url: str = source_url

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


@typing.runtime_checkable
class NoStorage(typing.Protocol):
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
