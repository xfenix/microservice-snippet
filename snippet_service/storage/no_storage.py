"""Dummy storage (no storage at all)."""
from __future__ import annotations

from .base import BasicStorage


class DummyStorage(BasicStorage):
    """No storage backend."""

    async def exists(self) -> bool:
        """Check is snippet already in storage."""
        return False

    async def save(self, _: dict) -> None:
        """Save snippet data in storage."""
        return

    async def fetch_raw(self) -> dict:
        """Fetch snippet data from storage."""
        return {}
