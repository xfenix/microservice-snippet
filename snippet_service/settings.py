"""All settings here.
"""
import pathlib

import envcast


PARSER_PROVIDER: str = envcast.env("SNIPPET_PARSER", "snippet_service.parser:AsyncBS")
STORAGE_PROVIDER: str = envcast.env("SNIPPET_STORAGE", "snippet_service.storage:Dummy")
COMEBACKER_ACTOR: str = envcast.env("SNIPPET_COMEBACKER", "")
FILE_STORAGE_ROOT: pathlib.Path = envcast.env("SNIPPET_FILE_STORAGE_ROOT", "/srv/storage/", type_cast=pathlib.Path)
