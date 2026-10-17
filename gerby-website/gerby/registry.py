"""Registry checks for import and web."""

import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from gerby_registry import (
    HISTORY,
    Evidence,
    RegistryError,
    check_database,
    check_rendered,
    labels_in,
    provenance,
    read,
    read_migrations,
    render,
    verified,
)


def import_preflight():
    rows = verified()
    output = read(ROOT / "gerby/tags")
    expected = render(
        rows,
        labels_in(ROOT / "gerby/book.tex"),
    )
    if output != expected:
        raise RegistryError(
            "Stale import registry"
        )
    check_rendered(
        output, ROOT / "gerby/document"
    )
    database = ROOT / "gerby/stack.sqlite"
    if database.exists():
        check_database(
            output,
            database,
            read_migrations(),
        )


@lru_cache(maxsize=4)
def evidence(history=HISTORY, root=ROOT):
    return Evidence(
        history, root, read_migrations()
    )


@lru_cache(maxsize=4)
def rendered(path):
    return read(path)


def describe(tag, path):
    """Provenance without guessed referents."""
    return provenance(
        tag, rendered(path), evidence()
    )
