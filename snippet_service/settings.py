"""All settings here.
"""
import os


PARSER_PROVIDER: str = os.getenv("SNIPPET_HTML_PARSER", "snippet_service.parser.BSParser")
STORAGE_PROVIDER: str = os.getenv("SNIPPET_STORAGE", "snippet_service.storage.NoStorage")
