"""Parser interfaces and realisations.
"""
from __future__ import annotations
import typing

import bs4


@typing.runtime_checkable
class GeneralInterface(typing.Protocol):
    """Interface contract.
    """

    def run_parsing(self) -> BasicParser:
        """Run/init parser. Need to be chainable method.
        """
        ...

    def extract_meta(self) -> BasicParser:
        """Extract snippet data. Need to be chainable method.
        """
        ...


class BasicParser:
    """Just basic parent.
    """

    def __init__(self, html_source: str) -> None:
        self._html_data: str = html_source


class BSParser(BasicParser):
    """Implementation of beautiful soup based parser.
    """

    def run_parsing(self) -> BSParser:
        """Init parser, default provider — lxml (its fastets).
        """
        self._parser: bs4.BeautifulSoup = bs4.BeautifulSoup(self._html_data, "lxml")
        return self

    def extract_meta(self) -> BSParser:
        """
        """
        return self
