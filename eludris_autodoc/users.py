"""This module implements Eludris API types related to users.

.. warning::
    This module was automatically generated.
"""
import enum
import typing

import attrs

from . import undefined


@attrs.define(kw_only=True, weakref_slot=False)
class ResetPassword:
    """The ResetPassword payload.

    This is used when the user wants to reset their password using a
    password reset code.

    Example
    -------
    ```json
    {
      "code": 234567,
      "email": "someemail@ma.il",
      "password": "wow such security"
    }
    ```
    """

    code: int = attrs.field()
    """The password reset code the user got emailed."""
    email: str = attrs.field()
    """The user's email."""
    password: str = attrs.field()
    """The user's new password."""


@attrs.define(kw_only=True, weakref_slot=False)
class PasswordDeleteCredentials:
    """The DeleteCredentials payload.

    This is used in multiple places in the API to provide extra
    credentials for deleting important user-related stuff.

    Example
    -------
    ```json
    {
      "password": "wowsuchpassword"
    }
    ```
    """

    password: str = attrs.field()


@attrs.define(kw_only=True, weakref_slot=False)
class UpdateUser:
    """The UpdateUser payload.

    Any field set to `null`, `undefined` or is missing will be disregarded
    and won't affect the user.

    Example
    -------
    ```json
    {
      "password": "authentícame por favor",
      "username": "yendli",
      "email": "yendli2@yemail.yom"
    }
    ```
    """

    password: str = attrs.field()
    """The user's current password for validation."""
    username: str | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The user's new username."""
    email: str | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The user's new email."""
    new_password: str | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )
    """The user's new password."""


@attrs.define(kw_only=True, weakref_slot=False)
class UserCreate:
    """The UserCreate payload.

    This is used when a user is initially first created.

    For authentication payloads check
    [`SessionCreate`].

    Example
    -------
    ```json
    {
      "username": "yendri",d
      "email": "yendri@llamoyendri.io",
      "password": "authentícame por favor" // don't actually use this as a password
    }
    ```
    """

    username: str = attrs.field()
    """The user's name.

    This is different to their `display_name` as it denotes how they're more formally
    referenced by the API.
    """
    email: str = attrs.field()
    """The user's email."""
    password: str = attrs.field()
    """The user's password."""


class StatusType(str, enum.Enum):
    """The type of a user's status.

    This is a string.
    """

    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    IDLE = "IDLE"
    BUSY = "BUSY"


@attrs.define(kw_only=True, weakref_slot=False)
class CreatePasswordResetCode:
    """The CreatePasswordResetCode payload.

    This is used when a user wants to generate a code
    to reset their password, most commonly because they forgot their old one.

    Example
    -------
    ```json
    {
      "email": "someemail@ma.il"
    }
    ```
    """

    email: str = attrs.field()
    """The user's email."""


@attrs.define(kw_only=True, weakref_slot=False)
class Status:
    """A user's status.

    Example
    -------
    ```json
    {
      "type": "BUSY",
      "text": "ayúdame por favor",
    }
    ```
    """

    type: StatusType = attrs.field()
    text: str | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)


@attrs.define(kw_only=True, weakref_slot=False)
class User:
    r"""The user payload.

    Example
    -------
    ```json
    {
      "id": 48615849987333,
      "username": "yendri",
      "display_name": "Nicolas",
      "social_credit": -69420,
      "status": {
        "type": "BUSY",
        "text": "ayúdame por favor",
       },
      "bio": "NICOLAAAAAAAAAAAAAAAAAAS!!!\n\n\nhttps://cdn.eludris.gay/static/nicolas.mp4",
      "avatar": 2255112175647,
      "banner": 2255049523230,
      "badges": 0,
      "permissions": 0
    }
    ```
    """

    id: int = attrs.field()
    """The user's ID."""
    username: str = attrs.field()
    """The user's username.

    This field has to be between 2 and 32 characters long.
    """
    display_name: str | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )
    """The user's display name.

    This field has to be between 2 and 32 characters long.
    """
    social_credit: int = attrs.field()
    """The user's social credit score."""
    status: Status = attrs.field()
    """The user's status."""
    bio: str | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The user's bio.

    The upper limit is the instance's [`InstanceInfo`] `bio_limit`.
    """
    avatar: int | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The user's avatar.

    This field has to be a valid file ID in the "avatar" bucket.
    """
    banner: int | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The user's banner.

    This field has to be a valid file ID in the "banner" bucket.
    """
    badges: int = attrs.field()
    """The user's badges as a bitfield."""
    permissions: int = attrs.field()
    """The user's instance-wide permissions as a bitfield."""
    email: str | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The user's email.

    This is only shown when the user queries their own data.
    """
    verified: bool | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The user's verification status.

    This is only shown when the user queries their own data.
    """


@attrs.define(kw_only=True, weakref_slot=False)
class UpdateUserProfile:
    """The UpdateUserProfile payload.

    This payload is used to update a user's profile.

    The abscence of a
    field or it being `undefined` means that it won't have an effect.

    Explicitly setting a field as
    `null` will clear it.

    Example
    -------
    ```json
    {
      "display_name": "HappyRu",
      "bio": "I am very happy!"
    }
    ```
    """

    display_name: str | None | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )
    """The user's new display name.

    This field has to be between 2 and 32 characters long.
    """
    status: str | None | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )
    """The user's new status.

    This field cannot be more than 150 characters long.
    """
    status_type: StatusType | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )
    """The user's new status type.

    This must be one of `ONLINE`, `OFFLINE`, `IDLE` and `BUSY`.
    """
    bio: str | None | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The user's new bio.

    The upper limit is the instance's [`InstanceInfo`] `bio_limit`.
    """
    avatar: int | None | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )
    """The user's new avatar.

    This field has to be a valid file ID in the "avatar" bucket.
    """
    banner: int | None | typing.Literal[undefined.Undefined] = attrs.field(
        default=undefined.Undefined,
    )
    """The user's new banner.

    This field has to be a valid file ID in the "banner" bucket.
    """
