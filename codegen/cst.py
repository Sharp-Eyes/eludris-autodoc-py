"""Impelementation of eludris-autodoc CST generation."""

import re
import typing

import libcst

from . import utils

__all__: typing.Sequence[str] = ("make_docstring", "parse_item")

ATTRS_DEFINE = libcst.Decorator(
    libcst.parse_expression("attrs.define(kw_only=True, weakref_slot=False)"),
)
ATTRS_FIELD = libcst.Attribute(libcst.Name("attrs"), libcst.Name("field"))

EQUALS = libcst.AssignEqual(libcst.SimpleWhitespace(""), libcst.SimpleWhitespace(""))

UNDEFINED = libcst.Attribute(
    libcst.Name("undefined"),
    libcst.Name("Undefined"),
)
UNDEFINED_ANN = libcst.Subscript(
    value=libcst.Attribute(
        libcst.Name("typing"),
        libcst.Name("Literal"),
    ),
    slice=[
        libcst.SubscriptElement(
            libcst.Index(UNDEFINED),
        ),
    ],
)

IPADDR_ANN = libcst.BinaryOperation(
    left=libcst.Attribute(
        libcst.Name("ipaddress"),
        libcst.Name("IPv4Address"),
    ),
    operator=libcst.BitOr(),
    right=libcst.Attribute(
        libcst.Name("ipaddress"),
        libcst.Name("IPv6Address"),
    ),
)


def to_upper_snake_case(name: str) -> str:
    """Convert camel_case names to UpperSnakeCase class names."""
    return name.title().replace("_", "")


def _get_inheritable_body(item: utils.AutodocItem) -> list[libcst.BaseStatement]:
    source_class = item.main_obj
    assert isinstance(source_class.body, libcst.IndentedBlock)

    inheritable: list[libcst.BaseStatement] = []
    for statement in source_class.body.body:
        match statement:
            case libcst.SimpleStatementLine(body=[libcst.Assign(_)]):
                inheritable.append(statement)

            case libcst.SimpleStatementLine(body=[libcst.AnnAssign(_)]):
                inheritable.append(statement)

            case _:
                pass

    return inheritable


def _make_rest_header(match: typing.Match[str]) -> str:
    header = match.group(1)
    return f"{header}\n{'-' * len(header)}\n"


def make_docstring(doc: str, *, indentation: int) -> libcst.SimpleStatementLine:
    """Make a docstring for a given item or method.

    This takes into account indentation and tries to convert autodoc markdown to rst.
    """
    # TODO: Make this work better by taking max line length into account, etc.
    indent = " " * 4 * indentation

    doc = (
        re.sub(
            r"### (\w+)\n\n",
            _make_rest_header,
            doc.replace("-----\n\n", ""),
        )
        .replace("\n", f"\n{indent}")
        .replace(". ", f".\n\n{indent}")
        .replace("> ", "")
        .replace(">\n", "\n")
    )

    strtype = "r" if "\\" in doc else ""
    end = f"\n{indent}" if "\n" in doc else ""

    return libcst.SimpleStatementLine(
        body=[
            libcst.Expr(
                libcst.SimpleString(
                    f'{strtype}"""{doc}{end}"""',
                ),
            ),
        ],
    )


def make_annotation(
    item_info: utils.ItemInfo,
    field_type: str,
    *,
    cache: typing.Mapping[str, utils.AutodocItem],
) -> libcst.BaseExpression:
    """Make type annotation for a given field."""
    is_list = field_type.endswith("[]")
    if is_list:
        field_type = field_type.removesuffix("[]")

    if field_type in utils.TYPE_MAPPING:
        raw_annotation = utils.TYPE_MAPPING[field_type]
        annotation = IPADDR_ANN if raw_annotation == "IpAddr" else libcst.Name(raw_annotation)

    else:
        category = cache[field_type].category
        if category == item_info["category"].lower():
            annotation = libcst.Name(f"{field_type}")

        else:
            annotation = libcst.Attribute(
                libcst.Name(f"{category}_m"),
                libcst.Name(field_type),
            )

    if not is_list:
        return annotation

    return libcst.Subscript(
        value=libcst.Attribute(
            libcst.Name("typing"),
            libcst.Name("Sequence"),
        ),
        slice=[
            libcst.SubscriptElement(
                libcst.Index(annotation),
            ),
        ],
    )


def make_field(
    item_info: utils.ItemInfo,
    field: utils.FieldInfo,
    *,
    cache: typing.Mapping[str, utils.AutodocItem],
) -> typing.Sequence[libcst.SimpleStatementLine]:
    """Make an attrs class field from an autodoc item field.

    This consists of a name, an annotation, and an attrs.field(...) expression.
    """
    annotation = make_annotation(item_info, field["type"], cache=cache)

    if field["nullable"]:
        annotation = libcst.BinaryOperation(
            left=annotation,
            operator=libcst.BitOr(),
            right=libcst.Name("None"),
        )

    args: list[libcst.Arg] = []
    if field["omittable"]:
        args.append(
            libcst.Arg(
                keyword=libcst.Name("default"),
                value=UNDEFINED,
                equal=EQUALS,
            ),
        )
        annotation = libcst.BinaryOperation(
            left=annotation,
            operator=libcst.BitOr(),
            right=UNDEFINED_ANN,
        )

    lines = [
        libcst.SimpleStatementLine(
            body=[
                libcst.AnnAssign(
                    target=libcst.Name(field["name"]),
                    annotation=libcst.Annotation(annotation),
                    value=libcst.Call(ATTRS_FIELD, args),
                ),
            ],
        ),
    ]

    if field["doc"]:
        lines.append(make_docstring(field["doc"], indentation=1))

    return lines


def parse_object_item(
    item_info: utils.ItemInfo,
    item: utils.ObjectItem,
    *,
    cache: typing.Mapping[str, utils.AutodocItem],
) -> libcst.ClassDef:
    """Parse an object item into an an attrs class."""
    fields: list[libcst.BaseStatement] = []

    if item_info["doc"]:
        fields.append(make_docstring(item_info["doc"], indentation=1))

    for field in item["fields"]:
        if not field["flattened"]:
            fields.extend(make_field(item_info, field, cache=cache))

        else:
            fields.extend(_get_inheritable_body(cache[field["type"]]))

    return libcst.ClassDef(
        libcst.Name(item_info["name"]),
        body=libcst.IndentedBlock(
            body=fields,
        ),
        decorators=[ATTRS_DEFINE],
    )


def _prepare_enum_variant(
    item_info: utils.ItemInfo,
    item: utils.EnumItem,
    variant: utils.EnumVariant,
    *,
    append_nodes: typing.Sequence[libcst.BaseStatement] | None = None,
) -> libcst.ClassDef:
    """Parse an enum item into a python attrs class."""
    if append_nodes is None:
        append_nodes = []

    doc = variant["doc"] or f"Please refer to {item_info['name']}."

    if item["tag"]:
        name = to_upper_snake_case(variant["name"]) + item_info["name"]

        return libcst.ClassDef(
            libcst.Name(name),
            body=libcst.IndentedBlock(
                body=[
                    make_docstring(doc, indentation=1),
                    libcst.SimpleStatementLine(
                        body=[
                            libcst.AnnAssign(
                                target=libcst.Name(item["tag"]),
                                annotation=libcst.Annotation(
                                    annotation=libcst.Subscript(
                                        value=libcst.Attribute(
                                            libcst.Name("typing"),
                                            libcst.Name("Literal"),
                                        ),
                                        slice=[
                                            libcst.SubscriptElement(
                                                libcst.Index(
                                                    libcst.SimpleString(f'"{variant["name"]}"'),
                                                ),
                                            ),
                                        ],
                                    ),
                                ),
                                value=libcst.Call(ATTRS_FIELD),
                            ),
                        ],
                    ),
                    *append_nodes,
                ],
            ),
            decorators=[ATTRS_DEFINE],
        )

    raise NotImplementedError


def parse_unit_enum_variant(
    item_info: utils.ItemInfo,
    item: utils.EnumItem,
    variant: utils.UnitEnumVariant,
) -> libcst.ClassDef:
    """Parse a unit enum into a python attrs class."""
    return _prepare_enum_variant(item_info, item, variant)


def parse_object_enum_variant(
    item_info: utils.ItemInfo,
    item: utils.EnumItem,
    variant: utils.ObjectEnumVariant,
    *,
    cache: typing.Mapping[str, utils.AutodocItem],
) -> libcst.ClassDef:
    """Parse an object enum variant into a python attrs class."""
    fields: list[libcst.BaseStatement] = []
    for field in variant["fields"]:
        if not field["flattened"]:
            fields.extend(make_field(item_info, field, cache=cache))

        else:
            fields.extend(_get_inheritable_body(cache[field["type"]]))

    return _prepare_enum_variant(
        item_info,
        item,
        variant,
        append_nodes=fields,
    )


def parse_tuple_enum_variant(
    item_info: utils.ItemInfo,
    item: utils.EnumItem,
    variant: utils.TupleEnumVariant,
    *,
    cache: typing.Mapping[str, utils.AutodocItem],
) -> libcst.ClassDef:
    """Parse a tuple enum variant into a python attrs class."""
    field_type = variant["field_type"]

    if item["content"]:
        annotation = make_annotation(item_info, field_type, cache=cache)

        return _prepare_enum_variant(
            item_info,
            item,
            variant,
            append_nodes=[
                libcst.SimpleStatementLine(
                    body=[
                        libcst.AnnAssign(
                            target=libcst.Name(item["content"]),
                            annotation=libcst.Annotation(annotation),
                            value=libcst.Call(ATTRS_FIELD),
                        ),
                    ],
                ),
            ],
        )

    return _prepare_enum_variant(
        item_info,
        item,
        variant,
        append_nodes=_get_inheritable_body(cache[field_type]),
    )


def parse_pure_unit_enum(item_info: utils.ItemInfo, item: utils.EnumItem) -> list[libcst.ClassDef]:
    """Parse a pure unit enum into a python Enum class."""
    body: list[libcst.BaseStatement] = []

    if item_info["doc"]:
        body.append(make_docstring(item_info["doc"], indentation=1))

    for variant in item["variants"]:
        body.append(
            libcst.SimpleStatementLine(
                body=[
                    libcst.Assign(
                        targets=[
                            libcst.AssignTarget(libcst.Name(variant["name"])),
                        ],
                        value=libcst.SimpleString(f'"{variant["name"]}"'),
                    ),
                ],
            ),
        )

        if variant["doc"]:
            body.append(make_docstring(variant["doc"], indentation=1))

    return [
        libcst.ClassDef(
            libcst.Name(item_info["name"]),
            body=libcst.IndentedBlock(
                body=body,
            ),
            bases=[
                libcst.Arg(libcst.Name("str")),
                libcst.Arg(
                    libcst.Attribute(
                        value=libcst.Name("enum"),
                        attr=libcst.Name("Enum"),
                    ),
                ),
            ],
        ),
    ]


def parse_enum_item(
    item_info: utils.ItemInfo,
    item: utils.EnumItem,
    *,
    cache: typing.Mapping[str, utils.AutodocItem],
) -> list[libcst.ClassDef] | list[libcst.ClassDef | libcst.SimpleStatementLine]:
    """Parse an enum item into python code.

    This automatically determines the type of enum item and parses it
    accordingly.

    In case the enum is *not* a pure unit enum, the last item in the returned
    list will be a union of all other items that make up the enum item. This is
    done to replicate the Rust-based eludris backend as closely as possible.
    """
    if not item["tag"]:
        return parse_pure_unit_enum(item_info, item)

    variants: list[libcst.ClassDef] = []

    for variant in item["variants"]:
        if variant["type"] == "unit":
            variants.append(parse_unit_enum_variant(item_info, item, variant))

        elif variant["type"] == "tuple":
            variants.append(
                parse_tuple_enum_variant(
                    item_info,
                    item,
                    variant,
                    cache=cache,
                ),
            )

        if variant["type"] == "object":
            variants.append(
                parse_object_enum_variant(
                    item_info,
                    item,
                    variant,
                    cache=cache,
                ),
            )

    variant_union = libcst.BinaryOperation(
        left=variants[-2].name,
        operator=libcst.BitOr(),
        right=variants[-1].name,
    )
    for variant in variants[-3::-1]:
        variant_union = libcst.BinaryOperation(
            left=variant.name,
            operator=libcst.BitOr(),
            right=variant_union,
        )

    body = [
        *variants,
        libcst.SimpleStatementLine(
            body=[
                libcst.Assign(
                    targets=[libcst.AssignTarget(libcst.Name(item_info["name"]))],
                    value=variant_union,
                ),
            ],
        ),
    ]

    if item_info["doc"]:
        body.append(make_docstring(item_info["doc"], indentation=0))

    return body


def _parse_item(
    item_info: utils.ItemInfo,
    *,
    cache: typing.Mapping[str, utils.AutodocItem],
) -> typing.Sequence[utils.ModuleCodeType]:
    item = item_info["item"]
    if item["type"] == "object":
        return [parse_object_item(item_info, item, cache=cache)]

    if item["type"] == "enum":
        return parse_enum_item(item_info, item, cache=cache)

    msg = f"What the heck is an {item['type']!r}!?"
    raise ValueError(msg)


def parse_item(
    item_info: utils.ItemInfo,
    *,
    cache: typing.MutableMapping[str, utils.AutodocItem],
) -> typing.Sequence[utils.ModuleCodeType]:
    """Parse an eludris-autodoc item.

    This automatically deals with caching the resulting types to deal with
    interdependent types.
    """
    items = _parse_item(item_info, cache=cache)
    cache[item_info["name"]].set_code(items)
    return items


def make_import(
    module: str,
    *,
    import_from: str | None = None,
    import_as: str | None = None,
) -> libcst.SimpleStatementLine:
    """Make CST for an import line.

    Note that this doesn't deal with optimally combining import lines. Since we
    run formatting tools over this anyways, we don't need to worry about this.
    """
    if not import_from:
        return libcst.SimpleStatementLine(
            body=[
                libcst.Import(
                    names=[libcst.ImportAlias(libcst.Name(module))],
                ),
            ],
        )

    asname = libcst.AsName(libcst.Name(import_as)) if import_as else None
    module_cst = (
        libcst.ImportStar()
        if module == "*"
        else [libcst.ImportAlias(libcst.Name(module), asname=asname)]
    )

    if import_from.startswith("."):
        from_ = import_from[1:]
        return libcst.SimpleStatementLine(
            body=[
                libcst.ImportFrom(
                    module=libcst.Name(from_) if from_ else None,
                    names=module_cst,
                    relative=[libcst.Dot()],
                ),
            ],
        )

    return libcst.SimpleStatementLine(
        body=[
            libcst.ImportFrom(
                module=libcst.Name(import_from),
                names=module_cst,
            ),
        ],
    )
