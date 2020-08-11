"""Comebackers module."""
import logging

import aiohttp

from snippet_service import exceptions, settings


LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


async def http_comebacker(meta_data: dict) -> None:
    """Basic HTTP comebacker."""
    if not settings.HTTP_COMEBACKER_DESTINATON:
        LOGGER_OBJ.warning("No comebacker destination, but http comebacker is enabled. Please, provide url")
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(settings.HTTP_COMEBACKER_DESTINATON, json=meta_data)
    except aiohttp.ClientError:
        LOGGER_OBJ.exception("Exception happens during snippet extraction")
        raise exceptions.HttpComebackerException
