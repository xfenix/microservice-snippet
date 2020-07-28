"""Core module.
"""
import typing
import logging

import bs4
import aiohttp
from fastapi import FastAPI, Depends

from snippet_service import settings
from snippet_service import helpers
from snippet_service import parser
from snippet_service import storage
from snippet_service import models


APP_OBJ: FastAPI = FastAPI()
LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


async def storage_dep():
    """Load storage backend.
    """
    actor_object: typing.Any = helpers.load_actor(settings.STORAGE_PROVIDER)()
    assert isinstance(
        actor_object, storage.GeneralInterface
    ), "Storage class doesnt provide necessary interface contract"
    await actor_object.init_storage()
    yield actor_object


def html_parser_dep():
    """Load html parser backends.
    """
    actor_object: typing.Any = helpers.load_actor(settings.PARSER_PROVIDER)()
    assert isinstance(
        actor_object, parser.GeneralInterface
    ), "HTML parser class doesnt provide necessary interface contract"
    yield actor_object


@APP_OBJ.get("/", response_model=models.SnippetAnswer)
async def fetch_remote_snippet(
    source_url: str, storage_actor=Depends(storage_dep), parser_actor=Depends(html_parser_dep)
):
    """Fetch snippet from url and store it in db.
    """
    await storage_actor.setup(source_url)
    if await storage_actor.exists():
        return models.SnippetAnswer(**await storage_actor.fetch())
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(source_url) as response:
                meta_tags: dict = parser_actor.setup(source_url, await response.text()).run_parsing().extract_meta()
                storage_actor.save(meta_tags)
                return models.SnippetAnswer(source_url=source_url, result=models.Status.JOB_OK)
    except aiohttp.ClientError as error_obj:
        LOGGER_OBJ.exception(f"Exception happens during snippet extraction: {error_obj}")
        return models.SnippetAnswer(source_url=source_url, result=models.Status.JOB_FAIL, result_info=str(error_obj))
