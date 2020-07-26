"""Core module.
"""
import bs4
import aiohttp
from fastapi import FastAPI


APP_OBJ: FastAPI = FastAPI()


@APP_OBJ.get("/")
async def fetch_remote_snippet(source_url: str):
    """Fetch snippet from url and store it in db.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(source_url) as response:
            parser_object = bs4.BeautifulSoup(await response.text(), "lxml")
            print(parser_object.find_all("meta"))
    return {"data": source_url}
