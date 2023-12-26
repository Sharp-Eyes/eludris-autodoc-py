"""This module implements Eludris API types related to errors.

.. warning::
    This module was automatically generated.
"""
import typing

import attrs


@attrs.define(kw_only=True, weakref_slot=False)
class SharedErrorData:
    """Shared fields between all error response variants."""

    status: int = attrs.field()
    """The HTTP status of the error."""
    message: str = attrs.field()
    """A brief explanation of the error."""


@attrs.define(kw_only=True, weakref_slot=False)
class UnauthorizedErrorResponse:
    """The error when the client is missing authorization.

    This error often occurs when the user
    doesn't pass in the required authentication or passes in invalid credentials.

    Example
    -------
    ```json
    {
      "type": "UNAUTHORIZED",
      "status": 401,
      "message": "The user is missing authentication or the passed credentials are invalid"
    }
    ```
    """

    type: typing.Literal["UNAUTHORIZED"] = attrs.field()
    status: int = attrs.field()
    message: str = attrs.field()


@attrs.define(kw_only=True, weakref_slot=False)
class ForbiddenErrorResponse:
    """The error when a client *has* been succesfully authorized but does not have the required
    permissions to execute an action.

    Example
    -------
    ```json
    {
      "type": "FORBIDDEN",
      "status": 403,
      "message": "The user is missing the requried permissions to execute this action",
    }
    ```
    """

    type: typing.Literal["FORBIDDEN"] = attrs.field()
    status: int = attrs.field()
    message: str = attrs.field()


@attrs.define(kw_only=True, weakref_slot=False)
class NotFoundErrorResponse:
    """The error when a client requests a resource that does not exist.

    Example
    -------
    ```json
    {
      "type": "NOT_FOUND",
      "status": 404,
      "message": "The requested resource could not be found"
    }
    ```
    """

    type: typing.Literal["NOT_FOUND"] = attrs.field()
    status: int = attrs.field()
    message: str = attrs.field()


@attrs.define(kw_only=True, weakref_slot=False)
class ConflictErrorResponse:
    """The error when a client's request causes a conflict, usually when they're trying to create
    something that already exists.

    Example
    -------
    ```json
    {
      "type": "CONFLICT",
      "status": 409,
      "message": "The request couldn't be completed due to conflicting with other data on the server",
      "item": "username",
    }
    ```
    """

    type: typing.Literal["CONFLICT"] = attrs.field()
    status: int = attrs.field()
    message: str = attrs.field()
    item: str = attrs.field()
    """The conflicting item."""


@attrs.define(kw_only=True, weakref_slot=False)
class MisdirectedErrorResponse:
    """The error when a server isn't able to reduce a response even though the client's request
    isn't explicitly wrong.

    This usually happens when an instance isn't configured to provide a
    response.

    Example
    -------
    ```json
    {
      "type": "MISDIRECTED",
      "status": 421,
      "message": "Misdirected request",
      "info": "The instance isn't configured to deal with unbased individuals"
    }
    ```
    """

    type: typing.Literal["MISDIRECTED"] = attrs.field()
    status: int = attrs.field()
    message: str = attrs.field()
    info: str = attrs.field()
    """Extra information about what went wrong."""


@attrs.define(kw_only=True, weakref_slot=False)
class ValidationErrorResponse:
    """The error when a request a client sends is incorrect and fails validation.

    Example
    -------
    ```json
    {
      "type": "VALIDATION",
      "status": 422,
      "message": "Invalid request",
      "value_name": "author",
      "info": "author name is a bit too cringe"
    }
    ```
    """

    type: typing.Literal["VALIDATION"] = attrs.field()
    status: int = attrs.field()
    message: str = attrs.field()
    value_name: str = attrs.field()
    """The name of the value that failed validation."""
    info: str = attrs.field()
    """Extra information about what went wrong."""


@attrs.define(kw_only=True, weakref_slot=False)
class RateLimitedErrorResponse:
    """The error when a client is rate limited.

    Example
    -------
    ```json
    {
      "type": "RATE_LIMITED",
      "status": 429,
      "message": "You have been rate limited",
      "retry_after": 1234
    }
    ```
    """

    type: typing.Literal["RATE_LIMITED"] = attrs.field()
    status: int = attrs.field()
    message: str = attrs.field()
    retry_after: int = attrs.field()
    """The amount of milliseconds you're still rate limited for."""


@attrs.define(kw_only=True, weakref_slot=False)
class ServerErrorResponse:
    """The error when the server fails to process a request.

    Getting this error means that it's the server's fault and not the client that the request
    failed.

    Example
    -------
    ```json
    {
      "type": "SERVER",
      "status": 500,
      "message": "Server encountered an unexpected error",
      "info": "Server got stabbed 28 times"
    }
    ```
    """

    type: typing.Literal["SERVER"] = attrs.field()
    status: int = attrs.field()
    message: str = attrs.field()
    info: str = attrs.field()
    """Extra information about what went wrong."""


ErrorResponse = (
    UnauthorizedErrorResponse
    | ForbiddenErrorResponse
    | NotFoundErrorResponse
    | ConflictErrorResponse
    | MisdirectedErrorResponse
    | ValidationErrorResponse
    | RateLimitedErrorResponse
    | ServerErrorResponse
)
"""All the possible error responses that are returned from Eludris HTTP microservices."""
