"""Pydantic models here."""
import enum
import typing

from pydantic import BaseModel


class Status(enum.Enum):
    """Service statuses."""

    JOB_OK: str = "ok"
    JOB_FAIL: str = "fail"


class SnippetBody(BaseModel):
    """Snippet data itself."""

    url: str
    domain: str
    title: str
    description: typing.Optional[str] = None
    image: typing.Optional[str] = None


class SnippetAnswer(BaseModel):
    """Main answer model wrapper."""

    source_url: str
    result: str = Status.JOB_OK
    result_info: typing.Optional[str]
    parse_time: typing.Optional[int]
    payload: typing.Optional[SnippetBody]
    is_comeback_goes_on: bool = False
