"""This module implements Eludris API types related to files.

.. warning::
    This module was automatically generated.
"""
import typing

import attrs

from . import undefined


@attrs.define(kw_only=True, weakref_slot=False)
class FileUpload:
    r"""The data format for uploading a file.

    This is a `multipart/form-data` form.

    Example
    -------
    ```sh
    curl \
      -F file=@trolley.mp4 \
      -F spoiler=true \
      https://cdn.eludris.gay/attachments/
    ```
    """

    file: object = attrs.field()
    spoiler: bool = attrs.field()


@attrs.define(kw_only=True, weakref_slot=False)
class TextFileMetadata:
    """Please refer to FileMetadata."""

    type: typing.Literal["TEXT"] = attrs.field()


@attrs.define(kw_only=True, weakref_slot=False)
class ImageFileMetadata:
    """Please refer to FileMetadata."""

    type: typing.Literal["IMAGE"] = attrs.field()
    width: int | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The image's width in pixels."""
    height: int | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The image's height in pixels."""


@attrs.define(kw_only=True, weakref_slot=False)
class VideoFileMetadata:
    """Please refer to FileMetadata."""

    type: typing.Literal["VIDEO"] = attrs.field()
    width: int | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The video's width in pixels."""
    height: int | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """The video's height in pixels."""


@attrs.define(kw_only=True, weakref_slot=False)
class OtherFileMetadata:
    """Please refer to FileMetadata."""

    type: typing.Literal["OTHER"] = attrs.field()


FileMetadata = TextFileMetadata | ImageFileMetadata | VideoFileMetadata | OtherFileMetadata
"""The enum representing all the possible Effis supported file metadatas.

Examples
--------
```json
{
  "type": "TEXT"
}
{
  "type": "IMAGE",
  "width": 5120,
  "height": 1440
}
{
  "type": "VIDEO",
  "width": 1920,
  "height": 1080
}
{
  "type": "OTHER"
}
```
"""


@attrs.define(kw_only=True, weakref_slot=False)
class FileData:
    """Represents a file stored on Effis.

    Example
    -------
    ```json
    {
      "id": 2195354353667,
      "name": "das_ding.png",
      "bucket": "attachments",
      "metadata": {
        "type": "IMAGE",
        "width": 1600,
        "height": 1600
      }
    }
    ```
    """

    id: int = attrs.field()
    """The file's ID."""
    name: str = attrs.field()
    """The file's name."""
    bucket: str = attrs.field()
    """The bucket the file is stored in."""
    spoiler: bool | typing.Literal[undefined.Undefined] = attrs.field(default=undefined.Undefined)
    """Whether the file is marked as a spoiler."""
    metadata: FileMetadata = attrs.field()
    """The [`FileMetadata`] of the file."""
