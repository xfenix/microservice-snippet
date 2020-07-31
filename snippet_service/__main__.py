"""Core module.
"""
import logging
import typing

import aiohttp
import bs4
from fastapi import Depends, FastAPI

from snippet_service import helpers, models, parser, settings, storage


APP_OBJ: FastAPI = FastAPI()
LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


@APP_OBJ.on_event("startup")
async def startup_event():
    """Validate interfaces on start.
    """
    assert isinstance(
        helpers.load_actor(settings.STORAGE_PROVIDER), storage.GeneralInterface
    ), "Storage class doesnt provide necessary interface contract"
    assert isinstance(
        helpers.load_actor(settings.PARSER_PROVIDER), parser.GeneralInterface
    ), "HTML parser class doesnt provide necessary interface contract"


async def storage_dep() -> typing.Generator[typing.Any]:
    """Load storage backend.
    """
    actor_object: typing.Any = helpers.load_actor(settings.STORAGE_PROVIDER)()
    await actor_object.init_storage()
    yield actor_object


def html_parser_dep() -> typing.Generator[typing.Any]:
    """Load html parser backends.
    """
    yield helpers.load_actor(settings.PARSER_PROVIDER)()


def comebacker_dep() -> typing.Optional[typing.Generator[typing.Any]]:
    """Load html parser backends.
    """
    yield helpers.load_actor(settings.COMEBACKER_ACTOR) if settings.COMEBACKER_ACTOR else None


@APP_OBJ.get("/", response_model=models.SnippetAnswer)
async def fetch_remote_snippet(
    source_url: str,
    storage_actor=Depends(storage_dep),
    parser_actor=Depends(html_parser_dep),
    comebacker_actor=Depends(comebacker_dep),
):
    """Fetch snippet from url and store it in db.
    """

    await storage_actor.setup(source_url)
    if await storage_actor.exists():
        return models.SnippetAnswer(source_url=source_url, payload=await storage_actor.fetch())
    try:
        extracted_meta: dict = await parser_actor.setup(source_url).fetch_and_extract()
        await storage_actor.save(extracted_meta)
        if comebacker_actor:
            pass
        return models.SnippetAnswer(source_url=source_url, payload=extracted_meta)
    except aiohttp.ClientError as error_obj:
        LOGGER_OBJ.exception(f"Exception happens during snippet extraction: {error_obj}")
        return models.SnippetAnswer(source_url=source_url, result=models.Status.JOB_FAIL, result_info=str(error_obj))
