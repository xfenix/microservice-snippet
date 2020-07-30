"""Parser interfaces and realisations.
"""
from __future__ import annotations
import typing

import aiohttp

from snippet_service import models


@typing.runtime_checkable
class GeneralInterface(typing.Protocol):
    """Interface contract.
    """

    def setup(self, source_url: str, html_source: str) -> typing.Type:
        """Basic setup. Need to be chainable method.
        """
        ...

    async def run_parsing(self) -> typing.Type:
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

    _html_data: str = ''

    def setup(self, source_url: str) -> None:
        self._url_source: str = source_url
        return self

    async def run_parsing(self):
        """Basic parsing realisation.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.source_url) as response:

