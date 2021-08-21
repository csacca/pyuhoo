"""Define package errors."""


class UhooError(Exception):
    """Define a base error."""

    pass


class RequestError(UhooError):
    """Define an error related to invalid requests."""

    pass


class UnauthorizedError(UhooError):
    """Define an error for 401 unauthorized responses"""

    pass


class ForbiddenError(UhooError):
    """Define an error for 403 forbidden responses"""

    pass
