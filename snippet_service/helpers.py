"""Basic helpers module.
"""
from __future__ import annotations
import typing
import importlib


def load_actor(full_class_path: str) -> typing.Any:
    """Load actor functonality.
    Parse paths like a.b.c, loads module a.b, get resource c from it and returns back.
    """
    parsed_paths: list = full_class_path.split(".")
    full_module_path: str = ".".join(parsed_paths[0:-1])
    class_name: str = parsed_paths[-1]
    return getattr(importlib.import_module(full_module_path), class_name)
