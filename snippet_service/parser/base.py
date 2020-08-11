"""Parser interfaces and realisations."""
from __future__ import annotations
import logging
import typing

import aiohttp

from snippet_service import exceptions, models


LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


@typing.runtime_checkable
class GeneralInterface(typing.Protocol):
    """Interface contract."""

    def setup(self, source_url: str) -> typing.Type:
        """Basic setup.

        Need to be chainable method.
        """
        ...

    async def fetch_and_extract(self) -> typing.Type:
        """Run/init parser.

        Need to be chainable method.
        """
        ...

    def extract_meta(self, response_body: str) -> models.SnippetBody:
        """Extract snippet data.

        Need to be chainable method.
        """
        ...


class BasicParser:
    """Just basic parent."""

    FIELDS_OF_INTEREST: typing.Tuple[str] = ("title", "description", "image")

    def __init__(self) -> None:
        self._url_source: str = ""

    def setup(self, source_url: str) -> None:
        """Simple setup method (now it just like setter)."""
        self._url_source = source_url
        return self

    async def fetch_and_extract(self):
        """Basic parsing realisation."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url_source) as response:
                    return self.extract_meta(await response.text())
        except aiohttp.ClientError as error_obj:
            LOGGER_OBJ.exception(f"Exception happens during snippet extraction: {error_obj} — {type(error_obj)}")
            raise exceptions.ParserFetchException
