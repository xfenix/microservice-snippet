"""Parser interfaces and realisations."""
from __future__ import annotations
import logging
import pathlib
from urllib import parse as url_lib

import aiofiles
import orjson
import xxhash

from .base import BasicStorage
from snippet_service import exceptions, settings


LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


class FileStorage(BasicStorage):
    """File storage backend.

    Stores snippet data in file system.
    """

    EXTENSION: str = ".cache.txt"
    _cache_full_path: pathlib.Path

    async def init_storage(self) -> None:
        """Run init."""
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
        """Check is snippet already in storage."""
        return self._cache_full_path.exists()

    async def save(self, snippet_data: dict) -> None:
        """Save snippet data in storage."""
        self._cache_full_path.mkdir(parents=True, exist_ok=True)
        try:
            async with aiofiles.open(str(self._cache_full_path), "w+") as file_handler:
                await file_handler.write(orjson.dumps(snippet_data))
        except (OSError, FileNotFoundError, IsADirectoryError, PermissionError, InterruptedError):
            LOGGER_OBJ.exception("Exception happens during file cache extraction")
            raise exceptions.StoreSaveException

    async def fetch_raw(self) -> dict:
        """Fetch snippet data from storage."""
        async with aiofiles.open(str(self._cache_full_path), "r") as file_handler:
            return orjson.loads(await file_handler.read())
