"""Define package errors."""


class UhooError(Exception):
    """Define a base error."""

    pass


class RequestError(UhooError):
    """Define an error related to invalid requests."""

    pass
