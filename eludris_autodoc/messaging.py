"""This module implements Eludris API types related to messaging.

.. warning::
    This module was automatically generated.
"""
import typing

import attrs

from . import undefined
from . import users as users_m


@attrs.define(kw_only=True, weakref_slot=False)
class MessageDisguise:
    """A temporary way to mask the message's author's name and avatar.

    This is mainly used for
    bridging and will be removed when webhooks are officially supported.

    Example
    -------
    ```json
    {
      "name": "Jeff",
      "avatar": "https://some-u.rl/to/some-image.png"
    }
    ```
    """

    name: str | None = attrs.field()
    """The name of the message's disguise."""
    avatar: str | None = attrs.field()
    """The URL of the message's disguise."""


@attrs.define(kw_only=True, weakref_slot=False)
class MessageCreate:
    """The MessageCreate payload.

    This is used when you want to create a message using the REST API.

    Example
    -------
    ```json
    {
      "content": "Hello, World!"
    }
    ```
    """

    content: str = attrs.field()
    """The message's content.

    This field has to be at-least 2 characters long.

    The upper limit
    is the instance's [`InstanceInfo`] `message_limit`.

    The content will be trimmed from leading and trailing whitespace.
    """
    _disguise: MessageDisguise | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )


@attrs.define(kw_only=True, weakref_slot=False)
class Message:
    """The Message payload.

    This is returned when you're provided information about a pre-existing
    message.

    Example
    -------
    ```json
    {
      "author": {
         "id": 48615849987333,
         "username": "mlynar",
         "social_credit": 9999.
         "badges": 256,
         "permissions": 8
      }
      "content": "Hello, World!"
    }
    ```
    """

    author: users_m.User = attrs.field()
    """The message's author."""
    content: str = attrs.field()
    _disguise: MessageDisguise | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )
