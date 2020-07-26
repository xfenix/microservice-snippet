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


APP_OBJ: FastAPI = FastAPI()
HTML_PARSER_ACTOR: typing.Any = helpers.load_actor(settings.PARSER_PROVIDER)
STORAGE_ACTOR: typing.Any = helpers.load_actor(settings.STORAGE_PROVIDER)
assert isinstance(
    HTML_PARSER_ACTOR, parser.GeneralInterface
), "HTML parser class doesnt provide necessary interface contract"
assert isinstance(STORAGE_ACTOR, storage.GeneralInterface), "Storage class doesnt provide necessary interface contract"


@APP_OBJ.get("/")
async def fetch_remote_snippet(source_url: str):
    """Fetch snippet from url and store it in db.
    """
    store_actor: typing.Any = STORAGE_ACTOR(source_url)
    if store_actor.exists():
        return store_actor.fetch()
    async with aiohttp.ClientSession() as session:
        async with session.get(source_url) as response:
            print(HTML_PARSER_ACTOR(await response.text()).run_parser().extract_meta())
            # store_actor.save(...)
    return {"data": source_url}
