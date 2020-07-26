"""Core module.
"""
import typing

import bs4
import aiohttp
from fastapi import FastAPI

from snippet_service import settings
from snippet_service import helpers


APP_OBJ: FastAPI = FastAPI()
HTML_PARSER_ACTOR: typing.Any = helpers.load_actor(settings.PARSER_PROVIDER)
STORAGE_ACTOR: typing.Any = helpers.load_actor(settings.STORAGE_PROVIDER)


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
