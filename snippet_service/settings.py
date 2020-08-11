"""All settings here."""
import pathlib

import envcast


SENTRY_DSN: str = envcast.env("SNIPPET_SENTRY_DSN")
API_PREFIX: str = envcast.env("SNIPPET_API_PREFIX").rstrip("/")
FILE_STORAGE_ROOT: pathlib.Path = envcast.env("SNIPPET_FILE_STORAGE_ROOT", "/srv/storage/", type_cast=pathlib.Path)
PARSER_PROVIDER: str = envcast.env("SNIPPET_PARSER", "snippet_service.parser:AsyncBSParser")
STORAGE_PROVIDER: str = envcast.env("SNIPPET_STORAGE", "snippet_service.storage:DummyStorage")

COMEBACKER_ACTOR: str = envcast.env("SNIPPET_COMEBACKER")
HTTP_COMEBACKER_DESTINATON: str = envcast.env("SNIPPET_HTTP_COMEBACKER_DESTINATON")
KAFKA_COMEBACKER_BOOTSTRAP: str = envcast.env("SNIPPET_KAFKA_COMEBACKER_BOOTSTRAP")
KAFKA_COMEBACKER_TOPIC: str = envcast.env("SNIPPET_KAFKA_COMEBACKER_TOPIC")
