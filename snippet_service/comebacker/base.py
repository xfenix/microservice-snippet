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

    async def format_request(self) -> typing.Type:
        """Run/init parser. Need to be chainable method.
        """
        ...

    async def submit_back(self) -> typing.Type:
        """Run/init parser. Need to be chainable method.
        """
        ...


class BasicComebacker:
    """Just basic parent.
    """
