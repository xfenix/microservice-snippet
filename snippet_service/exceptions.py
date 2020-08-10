"""Exceptions storage."""


class ParserFetchException(Exception):
    """Raises when somethings happend during connection."""


class StoreSaveException(Exception):
    """Raises when storage cant save cache."""


class HttpComebackerException(Exception):
    """Raises when cant reach comeback destination."""
