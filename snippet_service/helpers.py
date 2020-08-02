"""Basic helpers module.
"""
from __future__ import annotations
import importlib
import logging
import typing


LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


def load_actor(full_class_path: str) -> typing.Any:
    """Load actor functonality.
    Parse paths like a.b.c, loads module a.b, get resource c from it and returns back.
    """
    if ":" in full_class_path:
        full_module_path: str
        class_name: str
        full_module_path, class_name = full_class_path.split(":")
        return getattr(importlib.import_module(full_module_path), class_name)
    else:
        return importlib.import_module(full_class_path)


def load_actor_safe(full_class_path: str) -> typing.Any:
    """Load actor functonality.
    Parse paths like a.b.c, loads module a.b, get resource c from it and returns back.
    """
    try:
        return load_actor(full_class_path)
    except ModuleNotFoundError as exc:
        LOGGER_OBJ.error(f"Cant load module {full_class_path}")
        raise exc
