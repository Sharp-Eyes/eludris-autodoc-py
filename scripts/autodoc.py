"""Auto-generate code based on the current eludris-autodoc version."""

# TODO: Maybe automatically create a new commit and branch for each eludris version.

import argparse
import asyncio
import importlib

import aiohttp

from codegen import gen


def _check_import(*, version: str | None = None) -> bool:
    try:
        eludris_autodoc = importlib.import_module("eludris_autodoc")

        if eludris_autodoc.__version__ == version:
            print("Eludris-Autodoc is already up to date.")
            return True

    except Exception:  # noqa: BLE001
        print("Encountered error importing eludris-autodoc.")

    return False


async def _main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true", dest="force")

    args = parser.parse_args()

    async with aiohttp.ClientSession() as session:
        version, items = await gen.fetch_index(session=session)

        if not args.force and _check_import(version=version):
            return

        print("Regenerating autodoc types...")
        items = await gen.fetch_items(items, session=session)

    parsed = gen.parse_items(items)
    modules = gen.collect_module_items(parsed)
    modules["__init__"] = gen.make_init_module(modules, version=version)

    gen.write_modules(modules)
    _check_import()


def _sync_main() -> None:
    # Poetry requires sync entrypoints.
    asyncio.run(_main())


if __name__ == "__main__":
    _sync_main()
