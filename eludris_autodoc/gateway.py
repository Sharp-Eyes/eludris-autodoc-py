"""This module implements Eludris API types related to gateway.

.. warning::
    This module was automatically generated.
"""
import typing

import attrs

from . import instance as instance_m
from . import messaging as messaging_m
from . import users as users_m


@attrs.define(kw_only=True, weakref_slot=False)
class PingClientPayload:
    """The payload the client is supposed to periodically send the server to not get disconnected.

    The interval where these pings are supposed to be sent can be found in the `HELLO` payload
    of the [`ServerPayload`] enum.

    **Note**

    You are supposed to send your first ping in a connection after `RAND * heartbeat_interval` seconds,
    `RAND` being a random floating number between 0 and 1.

    This is done to avoid immediately overloading Pandemonium by connecting if it ever has to go down.

    Example
    -------
    ```json
    {
      "op": "PING"
    }
    ```
    """

    op: typing.Literal["PING"] = attrs.field()


@attrs.define(kw_only=True, weakref_slot=False)
class AuthenticateClientPayload:
    """The first payload the client is supposed to send.

    The data of this payload is expected to
    be a session token obtained from the [`create_session`] route.

    Example
    -------
    ```json
    {
      "op": "AUTHENTICATE",
      "d": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyMzQxMDY1MjYxMDU3LCJzZXNzaW9uX2lkIjoyMzQxMDgyNDMxNDg5fQ.j-nMmVTLXplaC4opGdZH32DUSWt1yD9Tm9hgB9M6oi4" // You're not supposed to use this example token (eckd)
    }
    ```
    """

    op: typing.Literal["AUTHENTICATE"] = attrs.field()
    d: str = attrs.field()


ClientPayload = PingClientPayload | AuthenticateClientPayload
"""Pandemonium websocket payloads sent by the client to the server."""


@attrs.define(kw_only=True, weakref_slot=False)
class PongServerPayload:
    """A [`ClientPayload`] `PING` payload response.

    Example
    -------
    ```json
    {
      "op": "PONG"
    }
    ```
    """

    op: typing.Literal["PONG"] = attrs.field()


@attrs.define(kw_only=True, weakref_slot=False)
class RateLimitServerPayload:
    """The payload sent when the client gets gateway rate limited.

    The client is supposed to wait `wait` milliseconds before sending any more events,
    otherwise they are disconnected.

    Example
    -------
    ```json
    {
      "op": "RATE_LIMIT",
      "d": {
        "wait": 1010 // 1.01 seconds
      }
    }
    ```
    """

    op: typing.Literal["RATE_LIMIT"] = attrs.field()
    wait: int = attrs.field()
    """The amount of milliseconds you have to wait before the rate limit ends"""


@attrs.define(kw_only=True, weakref_slot=False)
class HelloServerPayload:
    """The payload sent by the server when you initiate a new gateway connection.

    Example
    -------
    ```json
    {
      "op": "HELLO",
      "d": {
        "heartbeat_interval": 45000,
        "instance_info": {
          "instance_name": "EmreLand",
          "description": "More based than Oliver's instance (trust)",
          "version": "0.3.3",
          "message_limit": 2048,
          "oprish_url": "https://example.com",
          "pandemonium_url": "https://example.com",
          "effis_url": "https://example.com",
          "file_size": 20000000,
          "attachment_file_size": 100000000
        },
        "rate_limit": {
          "reset_after": 10,
          "limit": 5
        }
      }
    }
    ```
    """

    op: typing.Literal["HELLO"] = attrs.field()
    heartbeat_interval: int = attrs.field()
    """The amount of milliseconds your ping interval is supposed to be."""
    instance_info: instance_m.InstanceInfo = attrs.field()
    """The instance's info.

    This is the same payload you get from the [`get_instance_info`] payload without
    ratelimits
    """
    rate_limit: instance_m.RateLimitConf = attrs.field()
    """The pandemonium ratelimit info."""


@attrs.define(kw_only=True, weakref_slot=False)
class AuthenticatedServerPayload:
    """The payload sent when the client has successfully authenticated.

    This contains the data the
    user needs on startup.

    Example
    -------
    ```json
    {
      "op": "AUTHENTICATED",
      "user": {
        "id": 48615849987334,
        "username": "barbaz",
        "social_credit": 3,
        "badges": 0,
        "permissions": 0
      },
      "users": [
        {
          "id": 48615849987333,
          "username": "foobar",
          "social_credit": 42,
          "badges": 0,
          "permissions": 0
        }
      ],
    }
    ```
    """

    op: typing.Literal["AUTHENTICATED"] = attrs.field()
    user: users_m.User = attrs.field()
    users: typing.Sequence[users_m.User] = attrs.field()
    """The currently online users who are relavent to the connector."""


@attrs.define(kw_only=True, weakref_slot=False)
class UserUpdateServerPayload:
    """The payload received when a user updates themselves.

    This includes both user updates from
    the [`update_user`] endpoint and profile updates from the [`update_profile`] endpoint.

    Example
    -------
    ```json
    {
      "id": 48615849987333,
      "username": "foobar",
      "social_credit": 42,
      "badges": 0,
      "permissions": 0
    }
    ```
    """

    op: typing.Literal["USER_UPDATE"] = attrs.field()
    d: users_m.User = attrs.field()


@attrs.define(kw_only=True, weakref_slot=False)
class PresenceUpdateServerPayload:
    """The payload sent when a user's presence is updated.

    This is mainly used for when a user goes offline or online.

    Example
    -------
    ```json
    {
      "user_id": 48615849987333,
      "status": {
        "type": "IDLE",
        "text": "BURY THE LIGHT DEEP WITHIN"
      }
    }
    ```
    """

    op: typing.Literal["PRESENCE_UPDATE"] = attrs.field()
    user_id: int = attrs.field()
    status: users_m.Status = attrs.field()


@attrs.define(kw_only=True, weakref_slot=False)
class MessageCreateServerPayload:
    """The payload sent when the client receives a [`Message`].

    Example
    -------
    ```json
    {
      "op": "MESSAGE_CREATE",
      "d": {
        "author": "A Certain Woo",
        "content": "Woo!"
      }
    }
    ```
    """

    op: typing.Literal["MESSAGE_CREATE"] = attrs.field()
    d: messaging_m.Message = attrs.field()


ServerPayload = (
    PongServerPayload
    | RateLimitServerPayload
    | HelloServerPayload
    | AuthenticatedServerPayload
    | UserUpdateServerPayload
    | PresenceUpdateServerPayload
    | MessageCreateServerPayload
)
"""Pandemonium websocket payloads sent by the server to the client."""
