"""Actual code-gen implementation for eludris-autodoc."""

import asyncio
import collections
import pathlib
import subprocess
import typing

import aiohttp
import libcst
import yarl

from . import cst, utils

__all__: typing.Sequence[str] = (
    "fetch_index",
    "fetch_items",
    "parse_items",
    "collect_module_items",
    "make_init_module",
    "write_modules",
)

CWD: typing.Final[pathlib.Path] = pathlib.Path.cwd()
TARGET_DIR: typing.Final[pathlib.Path] = CWD / "eludris_autodoc"

DEFAULT_URL_BASE: typing.Final[yarl.URL] = yarl.URL(
    "https://refactor-autodoc-format.eludevs.pages.dev/autodoc/",
)

DEPENDENCY_RESOLUTION_MAX_ATTEMPTS: typing.Final[int] = 10

DEFAULT_IMPORTS = (
    cst.make_import("typing"),
    cst.make_import("attrs"),
    cst.make_import("enum"),
    cst.make_import("ipaddress"),
    cst.make_import("undefined", import_from="."),
)

MODULE_DOC_FMT = (
    '"""This module implements Eludris API types related to {category}.\n\n'
    ".. warning::\n"
    "    This module was automatically generated.\n"
    '"""'
)


def resolve_dependencies(entry_map: dict[str, utils.AutodocItem]) -> dict[str, utils.AutodocItem]:
    """Sort items such that no dependency conflicts appear down the line.

    Items are sorted in such a way that items without dependencies come first,
    and from there items are added only if all their dependencies are already
    in the sorted dict.

    If the items could not be ordered in a predefined number of attempts, a
    RuntimeError is raised.
    """
    sorted_entries = {name: entry for name, entry in entry_map.items() if not entry.dependencies}
    to_resolve = entry_map.keys() - sorted_entries

    for _ in range(DEPENDENCY_RESOLUTION_MAX_ATTEMPTS):
        for entry_name in to_resolve.copy():
            # Check if all dependencies have already been resolved.
            entry = entry_map[entry_name]
            if entry.dependencies.difference(sorted_entries):
                continue

            # Add entry to the back of the dict.
            to_resolve.remove(entry_name)
            sorted_entries[entry_name] = entry

        # If no unsorted entries remain, return.
        if not to_resolve:
            return sorted_entries

    msg = f"Failed to resolve dependency order. Unresolved: {to_resolve}"
    raise RuntimeError(msg)


async def fetch_index(
    *,
    url_base: yarl.URL | None = None,
    session: aiohttp.ClientSession,
) -> tuple[str, list[str]]:
    """Fetch the item index from the eludris-autodoc api."""
    if not url_base:
        url_base = DEFAULT_URL_BASE

    async with session.get(url_base / "index.json") as resp:
        data = await resp.json()
        return data["version"], data["items"]


async def fetch_item(
    item: str,
    *,
    url_base: yarl.URL | None = None,
    session: aiohttp.ClientSession,
) -> utils.AutodocItem:
    """Fetch an item from the eludris-autodoc api."""
    if not url_base:
        url_base = DEFAULT_URL_BASE

    async with session.get(url_base / item) as resp:
        return utils.AutodocItem.from_item(await resp.json())


async def fetch_items(
    items: typing.Sequence[str],
    *,
    url_base: yarl.URL | None = None,
    session: aiohttp.ClientSession,
) -> dict[str, utils.AutodocItem]:
    """Fetch multiple items from the eludris-autodoc-api."""
    if not url_base:
        url_base = DEFAULT_URL_BASE

    parsed_items = await asyncio.gather(
        *[
            fetch_item(item, session=session, url_base=url_base)
            for item in items
            if item.startswith("todel")
        ],
    )

    return resolve_dependencies({item.name: item for item in parsed_items})


def parse_items(items: dict[str, utils.AutodocItem]) -> dict[str, utils.AutodocItem]:
    """Parse the provided eludris-autodoc items into CST."""
    for item in items.values():
        item.code = cst.parse_item(item.data, cache=items)

    return items


def collect_module_items(items: dict[str, utils.AutodocItem]) -> dict[str, libcst.Module]:
    """Collect items into modules by category and add the necessary imports."""
    modules: dict[str, libcst.Module] = {}
    module_items: dict[str, collections.deque[utils.ModuleCodeType]] = {}
    module_imports: dict[str, set[str]] = {}

    for item in items.values():
        if item.category not in modules:
            module_items[item.category] = collections.deque()
            modules[item.category] = libcst.Module(module_items[item.category])
            module_imports[item.category] = set()

        if not item.code:
            msg = f"Encountered unparsed (or empty) item: {item.name!r}."
            raise RuntimeError(msg)

        module_items[item.category].extend(item.code)
        module_imports[item.category].update(
            items[dependency].category
            for dependency in item.dependencies
            if items[dependency].category != item.category
        )

    for module_name, imports in module_imports.items():
        module_code = module_items[module_name]
        module_code.extendleft(
            cst.make_import(import_, import_from=".", import_as=f"{import_}_m")
            for import_ in imports
        )
        module_code.extendleft(DEFAULT_IMPORTS)
        module_code.appendleft(
            libcst.SimpleStatementLine(
                body=[
                    libcst.Expr(
                        libcst.SimpleString(MODULE_DOC_FMT.format(category=module_name)),
                    ),
                ],
            ),
        )

    return modules


def make_init_module(modules: typing.Iterable[str], *, version: str) -> libcst.Module:
    """Make the __init__ module for the eludris-autodoc packages."""
    # TODO: actually make sure the link is valid
    doc = (
        f'"""Eludris-Autodoc version {version}.\n\n'
        "This module contains auto-generated types provided by Eludris autodoc,\n"
        "which can be found at https://docs.eludris.com/autodoc.\n"
        "The version of this module matches that of the Eludris API version for\n"
        " which it was generated.\n\n"
        ".. warning::\n"
        "    This module and all submodules except for `undefined` were\n"
        "    automatically generated.\n"
        '"""'
    )
    return libcst.Module(
        body=[
            libcst.SimpleStatementLine(
                body=[
                    libcst.Expr(
                        libcst.SimpleString(doc),
                    ),
                ],
            ),
            *DEFAULT_IMPORTS,
            *[cst.make_import("*", import_from=f".{module}") for module in modules],
            libcst.SimpleStatementLine(
                body=[
                    libcst.AnnAssign(
                        target=libcst.Name("__version__"),
                        annotation=libcst.Annotation(
                            libcst.Subscript(
                                value=libcst.Attribute(
                                    libcst.Name("typing"),
                                    libcst.Name("Final"),
                                ),
                                slice=[
                                    libcst.SubscriptElement(
                                        libcst.Index(libcst.Name("str")),
                                    ),
                                ],
                            ),
                        ),
                        value=libcst.SimpleString(f'"{version}"'),
                    ),
                ],
            ),
        ],
    )


def write_modules(modules: dict[str, libcst.Module]) -> None:
    """Write the parsed modules to files."""
    for module_name, module in modules.items():
        path = (TARGET_DIR / module_name).with_suffix(".py")
        path.write_text(module.code)

    for hook in ("ruff-format", "ruff"):
        subprocess.run(
            [f"pre-commit run {hook} --files eludris_autodoc/* -v"],
            cwd=str(CWD),
            shell=True,  # noqa: S602
            check=False,
        )
