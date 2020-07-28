"""Parser interfaces and realisations.
"""
from __future__ import annotations
import typing


@typing.runtime_checkable
class GeneralInterface(typing.Protocol):
    """Interface contract.
    """

    def setup(self, source_url: str, html_source: str) -> typing.Type:
        """Basic setup. Need to be chainable method.
        """
        ...

    def run_parsing(self) -> typing.Type:
        """Run/init parser. Need to be chainable method.
        """
        ...

    def extract_meta(self) -> typing.Type:
        """Extract snippet data. Need to be chainable method.
        """
        ...


class BasicParser:
    """Just basic parent.
    """

    def setup(self, source_url: str, html_source: str) -> None:
        self._html_data: str = html_source
        self._url_source: str = source_url
        return self
