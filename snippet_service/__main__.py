"""Core module."""
import asyncio
import logging
import typing

import fastapi
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from snippet_service import exceptions, helpers, models, settings


APP_OBJ: fastapi.FastAPI = fastapi.FastAPI()
ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()
LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


@APP_OBJ.on_event("startup")
def startup_event() -> None:
    """Validate interfaces on start."""
    helpers.validate_interfaces_on_start()


@ROUTER_OBJ.get("/", response_model=models.SnippetAnswer)
async def fetch_remote_snippet(
    source_url: str,
    force_renew: bool = False,
    storage_actor=fastapi.Depends(helpers.storage_dep),
    parser_actor=fastapi.Depends(helpers.html_parser_dep),
    comebacker_actor=fastapi.Depends(helpers.comebacker_dep),
):
    """Fetch snippet from url and store it in db."""
    result_store: typing.Optional[models.SnippetAnswer] = None
    await storage_actor.provide_url(source_url)
    if not force_renew and await storage_actor.exists():
        result_store = models.SnippetAnswer(source_url=source_url, payload=await storage_actor.fetch())

    if not result_store:
        try:
            extracted_meta: dict = await parser_actor.setup(source_url).fetch_and_extract()
        except exceptions.ParserFetchException as error_obj:
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
        asyncio.create_task(comebacker_actor(source_url, extracted_meta))
        result_store.is_comeback_goes_on = True

    typing.cast(models.SnippetAnswer, result_store)
    return result_store


APP_OBJ.include_router(ROUTER_OBJ, prefix=settings.API_PREFIX)
if settings.SENTRY_DSN:
    sentry_sdk.init(dsn=settings.SENTRY_DSN)
    APP_OBJ.add_middleware(SentryAsgiMiddleware)
