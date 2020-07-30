"""Parser interfaces and realisations.
"""
from __future__ import annotations
import typing

from snippet_service import models


@typing.runtime_checkable
class GeneralInterface(typing.Protocol):
    """Interface contract.
    """

    async def connect(self) -> typing.Type:
        """Basic setup. Need to be chainable method.
        """
        ...

    def format_response(self) -> typing.Type:
        """Format response for current session.
        """
        ...

    async def submit_back(self) -> None:
        """Submit request back.
        """
        ...


class BasicComebacker:
    """Just basic parent.
    """

    async def connect(self) -> typing.Type:
        """Do nothing.
        """
        return self

    def format_response(self) -> None:
        """Do nothing.
        """

    async def submit_back(self) -> None:
        """Do nothing.
        """
