"""Parser interfaces and realisations."""
from __future__ import annotations
import typing

import bs4

from .base import BasicParser
from snippet_service import models


class AsyncBSParser(BasicParser):
    """Implementation of beautiful soup based parser."""

    def extract_meta(self, response_body: str) -> models.SnippetBody:
        """Extracts data from downloaded page."""
        parser_obj: bs4.BeautifulSoup = bs4.BeautifulSoup(response_body, "lxml")
        return models.SnippetBody
