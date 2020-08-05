"""Core module.
"""
import logging
import typing

import aiohttp
import bs4
from fastapi import Depends, FastAPI

from snippet_service import exceptions, helpers, models, parser, settings, storage


APP_OBJ: FastAPI = FastAPI()
LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


@APP_OBJ.on_event("startup")
async def startup_event() -> None:
    """Validate interfaces on start."""
    assert isinstance(
        helpers.load_actor_safe(settings.STORAGE_PROVIDER), storage.GeneralInterface
    ), "Storage class doesnt provide necessary interface contract"
    assert isinstance(
        helpers.load_actor_safe(settings.PARSER_PROVIDER), parser.GeneralInterface
    ), "HTML parser class doesnt provide necessary interface contract"
    if settings.COMEBACKER_ACTOR:
        assert callable(helpers.load_actor_safe(settings.COMEBACKER_ACTOR)), "Comebacker is not callable"


async def storage_dep() -> typing.AsyncGenerator[typing.Any, None]:
    """Load storage backend."""
    actor_object: typing.Any = helpers.load_actor(settings.STORAGE_PROVIDER)()
    await actor_object.init_storage()
    yield actor_object


def html_parser_dep() -> typing.AsyncGenerator[typing.Any, None]:
    """Load html parser backends."""
    yield helpers.load_actor(settings.PARSER_PROVIDER)()


def comebacker_dep() -> typing.Optional[typing.AsyncGenerator[typing.Any, None]]:
    """Load html parser backends."""
    yield helpers.load_actor(settings.COMEBACKER_ACTOR) if settings.COMEBACKER_ACTOR else None


@APP_OBJ.get("/", response_model=models.SnippetAnswer)
async def fetch_remote_snippet(
    source_url: str,
    force_renew: bool = False,
    storage_actor=Depends(storage_dep),
    parser_actor=Depends(html_parser_dep),
    comebacker_actor=Depends(comebacker_dep),
):
    """Fetch snippet from url and store it in db."""
    result_store: typing.Optional[models.SnippetAnswer] = None
    await storage_actor.setup(source_url)
    if not force_renew and await storage_actor.exists():
        result_store = models.SnippetAnswer(source_url=source_url, payload=await storage_actor.fetch())

    if not result_store:
        try:
            extracted_meta: dict = await parser_actor.setup(source_url).fetch_and_extract()
        except exceptions.ParserFetchException:
            LOGGER_OBJ.exception(f"Exception happens during snippet extraction, url: {source_url}")
            return models.SnippetAnswer(
                source_url=source_url, result=models.Status.JOB_FAIL, result_info=str(error_obj)
            )
        try:
            await storage_actor.save(extracted_meta)
        except exceptions.StoreSaveException:
            # error during cache storing — is bad, but must no be deadly for main flow
            LOGGER_OBJ.error(f"Cant store cache for url {source_url}")
        result_store = models.SnippetAnswer(source_url=source_url, payload=extracted_meta)

    if comebacker_actor:
        comebacker_actor(source_url, extracted_meta)

    typing.cast(models.SnippetAnswer, result_store)
    return result_store
