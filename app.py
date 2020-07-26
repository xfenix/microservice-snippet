"""Core module.
"""
import typing

import bs4
import aiohttp
from fastapi import FastAPI

from snippet_service import settings
from snippet_service import helpers
from snippet_service import parser
from snippet_service import storage
from snippet_service import models


APP_OBJ: FastAPI = FastAPI()
HTML_PARSER_ACTOR: typing.Any = helpers.load_actor(settings.PARSER_PROVIDER)
STORAGE_ACTOR: typing.Any = helpers.load_actor(settings.STORAGE_PROVIDER)
assert isinstance(
    HTML_PARSER_ACTOR, parser.GeneralInterface
), "HTML parser class doesnt provide necessary interface contract"
assert isinstance(STORAGE_ACTOR, storage.GeneralInterface), "Storage class doesnt provide necessary interface contract"


@APP_OBJ.get("/", response_model=models.SnippetAnswer)
async def fetch_remote_snippet(source_url: str):
    """Fetch snippet from url and store it in db.
    """
    store_actor: typing.Any = STORAGE_ACTOR(source_url)
    if store_actor.exists():
        return store_actor.fetch()
    async with aiohttp.ClientSession() as session:
        async with session.get(source_url) as response:
            meta_tags: dict = HTML_PARSER_ACTOR(source_url, await response.text()).run_parsing().extract_meta()
            store_actor.save(meta_tags)
            return models.SnippetAnswer(source_url=source_url, result=models.Status.JOB_OK)
