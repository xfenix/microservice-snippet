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
        all_meta_tags: bs4.element.ResultSet = parser_obj.find_all("meta")
        one_element: bs4.element.Tag
        result_storage: typing.Dict[str, typing.Dict[str, str]] = {"og": {}, "native": {}}
        for one_element in all_meta_tags:
            result_group_key: str = ""
            property_name_clean: str = ""
            content_value: str = one_element.attrs["content"] if "content" in one_element.attrs else ""
            # figure out property name, that we should use for storing process and group for it
            # if there is no suitable tags, then we should store nothing
            if "property" in one_element.attrs and one_element.attrs["property"].startswith("og:"):
                property_name_clean = one_element.attrs["property"].replace("og:", "")
                result_group_key = "og"
            elif "name" in one_element.attrs and one_element.attrs["name"] in self.FIELDS_OF_INTEREST:
                property_name_clean = one_element.attrs["name"]
                result_group_key = "native"

            if result_group_key and property_name_clean and property_name_clean in self.FIELDS_OF_INTEREST:
                result_storage[result_group_key][property_name_clean] = content_value

        # TODO: choose og over native or vice versa
        return models.SnippetBody
