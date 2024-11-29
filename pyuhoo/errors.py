"""Define package errors."""


class UhooError(Exception):
    """Define a base error."""

    pass


class RequestError(UhooError):
    """Define an error related to invalid requests."""

    pass


class UnauthorizedError(RequestError):
    """Define an error for 401 unauthorized responses"""

    pass


class ForbiddenError(RequestError):
    """Define an error for 403 forbidden responses"""

    pass
