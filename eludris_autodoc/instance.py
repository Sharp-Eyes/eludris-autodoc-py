"""This module implements Eludris API types related to instance.

.. warning::
    This module was automatically generated.
"""
import typing

import attrs

from . import undefined


@attrs.define(kw_only=True, weakref_slot=False)
class EffisRateLimitConf:
    """Represents a single rate limit for Effis.

    Example
    -------
    ```json
    {
      "reset_after": 60,
      "limit": 5,
      "file_size_limit": 30000000
    }
    ```
    """

    reset_after: int = attrs.field()
    """The amount of seconds after which the rate limit resets."""
    limit: int = attrs.field()
    """The amount of requests that can be made within the `reset_after` interval."""
    file_size_limit: int = attrs.field()
    """The maximum amount of bytes that can be sent within the `reset_after` interval."""


@attrs.define(kw_only=True, weakref_slot=False)
class RateLimitConf:
    """Represents a single rate limit.

    Example
    -------
    ```json
    {
      "reset_after": 60,
      "limit": 30
    }
    ```
    """

    reset_after: int = attrs.field()
    """The amount of seconds after which the rate limit resets."""
    limit: int = attrs.field()
    """The amount of requests that can be made within the `reset_after` interval."""


@attrs.define(kw_only=True, weakref_slot=False)
class OprishRateLimits:
    """Rate limits that apply to Oprish (The REST API).

    Example
    -------
    ```json
    {
      "get_instance_info": {
        "reset_after": 5,
        "limit": 2
      },
      "create_message": {
        "reset_after": 5,
        "limit": 10
      },
      "create_user": {
      },
    }
    ```
    """

    get_instance_info: RateLimitConf = attrs.field()
    """Rate limits for the [`get_instance_info`] endpoint."""
    create_message: RateLimitConf = attrs.field()
    """Rate limits for the [`create_message`] endpoint."""
    create_user: RateLimitConf = attrs.field()
    """Rate limits for the [`create_user`] endpoint."""
    verify_user: RateLimitConf = attrs.field()
    """Rate limits for the [`verify_user`] endpoint."""
    get_user: RateLimitConf = attrs.field()
    """Rate limits for the [`get_self`], [`get_user`] and [`get_user_from_username`] endpoints."""
    guest_get_user: RateLimitConf = attrs.field()
    """Rate limits for the [`get_self`], [`get_user`] and [`get_user_from_username`] endpoints for
    someone who hasn't made an account.
    """
    update_user: RateLimitConf = attrs.field()
    """Rate limits for the [`update_user`] enpoint."""
    update_profile: RateLimitConf = attrs.field()
    """Rate limits for the [`update_profile`] enpoint."""
    delete_user: RateLimitConf = attrs.field()
    """Rate limits for the [`delete_user`] enpoint."""
    create_password_reset_code: RateLimitConf = attrs.field()
    """Rate limits for the [`create_password_reset_code`] enpoint."""
    reset_password: RateLimitConf = attrs.field()
    """Rate limits for the [`reset_password`] enpoint."""
    create_session: RateLimitConf = attrs.field()
    """Rate limits for the [`create_session`] endpoint."""
    get_sessions: RateLimitConf = attrs.field()
    """Rate limits for the [`get_sessions`] endpoint."""
    delete_session: RateLimitConf = attrs.field()
    """Rate limits for the [`delete_session`] endpoint."""


@attrs.define(kw_only=True, weakref_slot=False)
class EffisRateLimits:
    """Rate limits that apply to Effis (The CDN).

    Example
    -------
    ```json
    {
      "assets": {
        "reset_after": 60,
        "limit": 5,
        "file_size_limit": 30000000
      },
      "attachments": {
        "reset_after": 180,
        "limit": 20,
        "file_size_limit": 500000000
      },
      "fetch_file": {
        "reset_after": 60,
        "limit": 30
      }
    }
    ```
    """

    assets: EffisRateLimitConf = attrs.field()
    """Rate limits for the asset buckets."""
    attachments: EffisRateLimitConf = attrs.field()
    """Rate limits for the attachment bucket."""
    fetch_file: RateLimitConf = attrs.field()
    """Rate limits for the file fetching endpoints."""


@attrs.define(kw_only=True, weakref_slot=False)
class InstanceRateLimits:
    """Represents all rate limits that apply to the connected Eludris instance.

    ### Example
    ```json
    {
      "oprish": {
        "info": {
          "reset_after": 5,
          "limit": 2
        },
        "message_create": {
          "reset_after": 5,
          "limit": 10
        },
        "rate_limits": {
          "reset_after": 5,
          "limit": 2
        }
      },
      "pandemonium": {
        "reset_after": 10,
        "limit": 5
      },
      "effis": {
        "assets": {
          "reset_after": 60,
          "limit": 5,
          "file_size_limit": 30000000
        },
        "attachments": {
          "reset_after": 180,
          "limit": 20,
          "file_size_limit": 500000000
        },
        "fetch_file": {
          "reset_after": 60,
          "limit": 30
        }
      }
    }
    ```
    """

    oprish: OprishRateLimits = attrs.field()
    """The instance's Oprish rate limit information (The REST API)."""
    pandemonium: RateLimitConf = attrs.field()
    """The instance's Pandemonium rate limit information (The WebSocket API)."""
    effis: EffisRateLimits = attrs.field()
    """The instance's Effis rate limit information (The CDN)."""


@attrs.define(kw_only=True, weakref_slot=False)
class InstanceInfo:
    """Represents information about the connected Eludris instance.

    Example
    -------
    ```json
    {
      "instance_name": "eludris",
      "description": "The *almost* official Eludris instance - ooliver.",
      "version": "0.3.2",
      "message_limit": 2000,
      "oprish_url": "https://api.eludris.gay",
      "pandemonium_url": "wss://ws.eludris.gay/",
      "effis_url": "https://cdn.eludris.gay",
      "file_size": 20000000,
      "attachment_file_size": 25000000,
      "rate_limits": {
        "oprish": {
          "info": {
            "reset_after": 5,
            "limit": 2
          },
          "message_create": {
            "reset_after": 5,
            "limit": 10
          },
          "rate_limits": {
            "reset_after": 5,
            "limit": 2
          }
        },
        "pandemonium": {
          "reset_after": 10,
          "limit": 5
        },
        "effis": {
          "assets": {
            "reset_after": 60,
            "limit": 5,
            "file_size_limit": 30000000
          },
          "attachments": {
            "reset_after": 180,
            "limit": 20,
            "file_size_limit": 500000000
          },
          "fetch_file": {
            "reset_after": 60,
            "limit": 30
          }
        }
      }
    }
    ```
    """

    instance_name: str = attrs.field()
    """The instance's name."""
    description: str | None = attrs.field()
    """The instance's description.

    This is between 1 and 2048 characters long.
    """
    version: str = attrs.field()
    """The instance's Eludris version."""
    message_limit: int = attrs.field()
    """The maximum length of a message's content."""
    oprish_url: str = attrs.field()
    """The URL of the instance's Oprish (REST API) endpoint."""
    pandemonium_url: str = attrs.field()
    """The URL of the instance's Pandemonium (WebSocket API) endpoint."""
    effis_url: str = attrs.field()
    """The URL of the instance's Effis (CDN) endpoint."""
    file_size: int = attrs.field()
    """The maximum file size (in bytes) of an asset."""
    attachment_file_size: int = attrs.field()
    """The maximum file size (in bytes) of an attachment."""
    email_address: str | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )
    """The instance's email address if any."""
    rate_limits: InstanceRateLimits | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )
    """The rate limits that apply to the connected Eludris instance.

    This is not present if the `rate_limits` query parameter is not set.
    """
