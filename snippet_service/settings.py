"""All settings here."""
import pathlib

import envcast


PARSER_PROVIDER: str = envcast.env("SNIPPET_PARSER", "snippet_service.parser:AsyncBSParser")
STORAGE_PROVIDER: str = envcast.env("SNIPPET_STORAGE", "snippet_service.storage:DummyStorage")
COMEBACKER_ACTOR: str = envcast.env("SNIPPET_COMEBACKER")
COMEBACKER_DESTINATON: str = envcast.env("SNIPPTER_COMEBACKER_DESTINATION")
API_PREFIX: str = envcast.env("SNIPPET_API_PREFIX").rstrip("/")
FILE_STORAGE_ROOT: pathlib.Path = envcast.env("SNIPPET_FILE_STORAGE_ROOT", "/srv/storage/", type_cast=pathlib.Path)
