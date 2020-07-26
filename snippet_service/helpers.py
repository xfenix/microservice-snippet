"""Basic helpers module.
"""
from __future__ import annotations
import typing
import importlib


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
