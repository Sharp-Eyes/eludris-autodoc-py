"""Utilities for eludris-autodoc code-gen."""

import typing

import attrs
import libcst

__all__: typing.Sequence[str] = ("TYPE_MAPPING", "AutodocItem")


ModuleCodeType = libcst.BaseCompoundStatement | libcst.SimpleStatementLine


TYPE_MAPPING: dict[str, str] = {
    "String": "str",
    "str": "str",
    "u8": "int",
    "u16": "int",
    "u32": "int",
    "u64": "int",
    "u128": "int",
    "usize": "int",
    "i8": "int",
    "i16": "int",
    "i32": "int",
    "i64": "int",
    "i128": "int",
    "isize": "int",
    "bool": "bool",
    "IpAddr": "IpAddr",
    "file": "object",
}


class FieldInfo(typing.TypedDict):
    name: str
    doc: str | None
    type: str
    nullable: bool
    omittable: bool
    flattened: bool


class ObjectItem(typing.TypedDict):
    type: typing.Literal["object"]
    fields: typing.Sequence[FieldInfo]


class UnitEnumVariant(typing.TypedDict):
    type: typing.Literal["unit"]
    name: str
    doc: str | None


class TupleEnumVariant(typing.TypedDict):
    type: typing.Literal["tuple"]
    name: str
    doc: str | None
    field_type: str


class ObjectEnumVariant(typing.TypedDict):
    type: typing.Literal["object"]
    name: str
    doc: str | None
    fields: typing.Sequence[FieldInfo]


EnumVariant = UnitEnumVariant | TupleEnumVariant | ObjectEnumVariant


class EnumItem(typing.TypedDict):
    type: typing.Literal["enum"]
    tag: str | None
    untagged: bool
    content: str | None
    variants: list[EnumVariant]


class ItemInfo(typing.TypedDict):
    name: str
    doc: str | None
    category: str
    hidden: bool
    package: str
    item: ObjectItem | EnumItem


@attrs.define(kw_only=True)
class AutodocItem:
    """Representation of a singular top-level eludris-autodoc item."""

    data: ItemInfo
    """Metadata that applies to any kind of eludris-autodoc item."""
    dependencies: set[str]
    """A set of names of all other items that this item needs.

    This is used internally to figure out which other modules need to be
    imported for this item to work.
    """

    code: typing.Sequence[ModuleCodeType] = attrs.field(factory=list, init=False)
    """The CST for this item."""
    _main_obj: ModuleCodeType | None = attrs.field(default=None, init=False)

    @property
    def name(self) -> str:
        """The name of this item."""
        return self.data["name"]

    @property
    def category(self) -> str:
        """The category of this item.

        Items are grouped into python modules by category.
        """
        return self.data["category"].lower()

    @property
    def main_obj(self) -> ModuleCodeType:
        """The main object of this item."""
        if self._main_obj:
            return self._main_obj

        msg = (
            f"The item with name {self.name} has not yet been finalised."
            " Ensure AutodocItem.set_code is run before accessing AutodocItem.main_obj."
        )
        raise RuntimeError(msg)

    @classmethod
    def from_item(cls, item_info: ItemInfo) -> "AutodocItem":
        """Create an AutodocItem from an ItemInfo as it is returned from the eludris-autodoc API."""
        item = item_info["item"]
        if item["type"] == "object":
            dependencies = _get_object_dependencies(item)

        else:
            dependencies: set[str] = set()
            for variant in item["variants"]:
                if variant["type"] == "tuple":
                    dependencies.add(_extract_type_name(variant["field_type"]))

                elif variant["type"] == "object":
                    dependencies.update(_get_object_dependencies(variant))

        dependencies -= TYPE_MAPPING.keys()

        return cls(data=item_info, dependencies=dependencies)

    def set_code(self, items: typing.Sequence[ModuleCodeType]) -> None:
        """Set the generated CST for this item.

        This also makes ``self.main_obj`` available.
        """
        self.code = items

        if len(items) == 1:
            # Object or actual python enum.
            self._main_obj = items[0]

        else:
            # Enum, last item is the Union of all enum types.
            self._main_obj = items[-1]


def _get_object_dependencies(item: ObjectItem) -> set[str]:
    dependencies: set[str] = set()

    for field in item["fields"]:
        dep_name = _extract_type_name(field["type"])
        if field["flattened"] or (field["type"] not in TYPE_MAPPING):
            dependencies.add(dep_name)

    return dependencies


def _extract_type_name(name: str) -> str:
    return name.removesuffix("[]")
