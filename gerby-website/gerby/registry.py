"""Registry checks for import and web."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from gerby_registry import (
    RegistryError,
    check_database,
    check_rendered,
    labels_in,
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


def retired(tag, path):
    row = read(path).get(tag)
    return row is not None and not row[1]
