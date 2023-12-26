"""This module implements Eludris API types related to sessions.

.. warning::
    This module was automatically generated.
"""
import ipaddress

import attrs


@attrs.define(kw_only=True, weakref_slot=False)
class SessionCreate:
    """The SessionCreate payload.

    This is used to authenticate a user and obtain a token to interface with the API.

    Example
    -------
    ```json
    {
      "identifier": "yendri",
      "password": "authentícame por favor",
      "platform": "linux",
      "client": "pilfer"
    }
    ```
    """

    identifier: str = attrs.field()
    """The session user's identifier.

    This can be either their email or username.
    """
    password: str = attrs.field()
    """The session user's password."""
    platform: str = attrs.field()
    """The session's platform (linux, windows, mac, etc.)"""
    client: str = attrs.field()
    """The client the session was created by."""


@attrs.define(kw_only=True, weakref_slot=False)
class Session:
    """The session payload.

    The user should ideally have one session for every client they have on every device.

    Example
    -------
    ```json
    {
      "id": 2312155037697,
      "user_id": 2312155693057,
      "platform": "linux",
      "client": "pilfer"
    }
    ```
    """

    id: int = attrs.field()
    """The session's ID."""
    user_id: int = attrs.field()
    """The session user's ID."""
    platform: str = attrs.field()
    """The session's platform (linux, windows, mac, etc.)"""
    client: str = attrs.field()
    """The client the session was created by."""
    ip: ipaddress.IPv4Address | ipaddress.IPv6Address = attrs.field()
    """The session's creation IP address."""


@attrs.define(kw_only=True, weakref_slot=False)
class SessionCreated:
    """The response to a [`SessionCreate`].

    Example
    -------
    ```json
    {
      "token": "",
      "session": {
        "indentifier": "yendri",
        "password": "authentícame por favor",
        "platform": "linux",
        "client": "pilfer"
      }
    }
    ```
    """

    token: str = attrs.field()
    """The session's token.

    This can be used by the user to properly interface with the API.
    """
    session: Session = attrs.field()
    """The session object that was created."""
