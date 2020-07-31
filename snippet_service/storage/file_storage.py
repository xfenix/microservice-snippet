"""Parser interfaces and realisations.
"""
from __future__ import annotations
from urllib import parse as url_lib

import aiofile
import orjson
import xxhash

from .base import BasicStorage
from snippet_service import settings


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
        async with aiofile.AIOFile(str(self._cache_full_path), "w+") as file_handler:
            await file_handler.write(orjson.dumps(snippet_data))

    async def fetch_raw(self) -> dict:
        """Fetch snippet data from storage.
        """
        async with aiofile.AIOFile(str(self._cache_full_path), "r") as file_handler:
            return orjson.loads(await file_handler.read())
