"""Basic helpers module."""
from __future__ import annotations
import importlib
import logging
import typing

from snippet_service import parser, settings, storage


LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


def load_actor(full_class_path: str) -> typing.Any:
    """Load actor functonality.

    Parse paths like a.b.c, loads module a.b, get resource c from it and
    returns back.
    """
    if ":" in full_class_path:
        full_module_path: str
        class_name: str
        full_module_path, class_name = full_class_path.split(":")
        return getattr(importlib.import_module(full_module_path), class_name)
    return importlib.import_module(full_class_path)


def load_actor_safe(full_class_path: str) -> typing.Any:
    """Load actor functonality.

    Parse paths like a.b.c, loads module a.b, get resource c from it and
    returns back.
    """
    try:
        return load_actor(full_class_path)
    except ModuleNotFoundError as exc:
        LOGGER_OBJ.error(f"Cant load module {full_class_path}")
        raise exc


async def storage_dep() -> typing.AsyncGenerator[typing.Any, None]:
    """Load storage backend."""
    actor_object: typing.Any = load_actor(settings.STORAGE_PROVIDER)()
    await actor_object.init_storage()
    yield actor_object


def html_parser_dep() -> typing.AsyncGenerator[typing.Any, None]:
    """Load html parser backends."""
    yield load_actor(settings.PARSER_PROVIDER)()


def comebacker_dep() -> typing.Optional[typing.AsyncGenerator[typing.Any, None]]:
    """Load html parser backends."""
    yield load_actor(settings.COMEBACKER_ACTOR) if settings.COMEBACKER_ACTOR else None


def validate_interfaces_on_start() -> None:
    """Validate interfaces."""
    assert isinstance(
        load_actor_safe(settings.STORAGE_PROVIDER), storage.GeneralInterface
    ), "Storage class doesnt provide necessary interface contract"
    assert isinstance(
        load_actor_safe(settings.PARSER_PROVIDER), parser.GeneralInterface
    ), "HTML parser class doesnt provide necessary interface contract"
    if settings.COMEBACKER_ACTOR:
        assert callable(load_actor_safe(settings.COMEBACKER_ACTOR)), "Comebacker is not callable"
