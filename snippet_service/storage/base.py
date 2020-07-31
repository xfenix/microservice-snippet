"""Basic storage module.
"""
from __future__ import annotations
import typing


@typing.runtime_checkable
class GeneralInterface(typing.Protocol):
    """Interface contract.
    """

    async def setup(self, source_url: str) -> typing.Type:
        """Run init per snippet request.
        """
        ...

    async def init_storage(self) -> None:
        """Run global init.
        """
        ...

    async def exists(self) -> bool:
        """Check is snippet already in storage.
        """
        ...

    async def save(self, snippet_data: dict) -> None:
        """Save raw json data in storage.
        """
        ...

    async def fetch_raw(self) -> dict:
        """Fetch raw json data from storage.
        """
        ...

    async def fetch(self) -> model.SnippetBody:
        """Fetch snippet data from storage.
        """
        ...


class BasicStorage:
    """Very simple parent.
    """

    async def init_storage(self) -> None:
        """By default do nothing.
        """

    async def setup(self, source_url: str) -> BasicStorage:
        """Setup basic attr.
        """
        self._data_url: str = source_url
        return self

    async def fetch(self) -> model.SnippetBody:
        """Fetch snippet data from storage.
        """
        return models.SnippetBody(**await self.fetch_raw())
