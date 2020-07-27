"""Parser interfaces and realisations.
"""
from __future__ import annotations
import typing
from urllib import parse as url_lib

import xxhash
import orjson
import aiofile

from snippet_service import settings


@typing.runtime_checkable
class GeneralInterface(typing.Protocol):
    """Interface contract.
    """

    async def init_storage(self) -> None:
        """Run init.
        """
        ...

    async def exists(self) -> bool:
        """Check is snippet already in storage.
        """
        ...

    async def save(self, snippet_data: dict) -> None:
        """Save snippet data in storage.
        """
        ...

    async def fetch(self) -> dict:
        """Fetch snippet data from storage.
        """
        ...


class BasicStorage:
    """Very simple parent.
    """

    def __init__(self, source_url: str) -> None:
        self._data_url: str = source_url

    async def init_storage(self) -> None:
        """Run init basic.
        """


class NoStorage(BasicStorage):
    """No storage backend.
    """

    async def exists(self) -> bool:
        """Check is snippet already in storage.
        """
        return False

    async def save(self, snippet_data: dict) -> None:
        """Save snippet data in storage.
        """
        return

    async def fetch(self) -> dict:
        """Fetch snippet data from storage.
        """
        return {}


class FileStorage(BasicStorage):
    """File storage backend.
    Stores snippet data in file system.
    """

    EXTENSION: str = ".cache.txt"

    async def init_storage(self) -> None:
        """Run init.
        """
        _hash_digest: str = xxhash.xxh64(self._data_url).hexdigest()
        _url_parts: url_lib.ParseResult = url_lib.urlparse(self._data_url)
        self._cache_full_path: pathlib.Path = (
            settings.FILE_STORAGE_ROOT.joinpath(_url_parts.domain)
            .joinpath(_hash_digest[:2])
            .joinpath(_hash_digest[2:4])
            .joinpath(_hash_digest[4:6])
            .joinpath(f"{_hash_digest}{self.EXTENSION}")
        )

    async def exists(self) -> bool:
        """Check is snippet already in storage.
        """
        return self._cache_full_path.exists()

    async def save(self, snippet_data: dict) -> None:
        """Save snippet data in storage.
        """
        self._cache_full_path.mkdir(parents=True, exist_ok=True)
        # self._cache_full_path.write_text(orjson.dumps(snippet_data))
        async with aiofile.AIOFile(str(self._cache_full_path), "w+") as file_handler:
            await file_handler.write(orjson.dumps(snippet_data))

    async def fetch(self) -> dict:
        """Fetch snippet data from storage.
        """
        return orjson.loads(self._cache_full_path.read_text())
