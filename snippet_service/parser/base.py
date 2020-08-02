"""Parser interfaces and realisations.
"""
from __future__ import annotations
import typing

import aiohttp

from snippet_service import exceptions, models


@typing.runtime_checkable
class GeneralInterface(typing.Protocol):
    """Interface contract.
    """

    def setup(self, source_url: str) -> typing.Type:
        """Basic setup. Need to be chainable method.
        """
        ...

    async def fetch_and_extract(self) -> typing.Type:
        """Run/init parser. Need to be chainable method.
        """
        ...

    def extract_meta(self) -> models.SnippetBody:
        """Extract snippet data. Need to be chainable method.
        """
        ...


class BasicParser:
    """Just basic parent.
    """

    def setup(self, source_url: str) -> None:
        self._url_source: str = source_url
        return self

    async def fetch_and_extract(self):
        """Basic parsing realisation.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url_source) as response:
                    return self.extract_meta(await response.text())
        except aiohttp.ClientError as error_obj:
            LOGGER_OBJ.exception(f"Exception happens during snippet extraction: {error_obj} — {type(error_obj)}")
            raise exceptions.ParserFetchException
