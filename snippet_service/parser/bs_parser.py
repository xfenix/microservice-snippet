"""Parser interfaces and realisations.
"""
from __future__ import annotations
import typing

import bs4

from .base import BasicParser
from snippet_service import models


class BSParser(BasicParser):
    """Implementation of beautiful soup based parser.
    """

    def run_parsing(self) -> BSParser:
        """Init parser, default provider — lxml (its fastets).
        """
        self._parser: bs4.BeautifulSoup = bs4.BeautifulSoup(self._html_data, "lxml")
        return self

    def extract_meta(self) -> models.SnippetBody:
        """
        """
        return models.SnippetBody
