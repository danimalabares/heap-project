#!/usr/bin/env python3
"""Render or explicitly allocate tags."""

import argparse
import fcntl
from pathlib import Path

from gerby_registry import (
    HISTORY,
    ROOT,
    SOURCE,
    atomic_write,
    labels_in,
    render,
    record,
    serialize,
    verified,
    RegistryError,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "texfile",
        nargs="?",
        default="gerby/book.tex",
    )
    parser.add_argument(
        "--tags", default=str(SOURCE)
    )
    parser.add_argument(
        "--history", default=str(HISTORY)
    )
    parser.add_argument(
        "--root", default=str(ROOT)
    )
    parser.add_argument("--output")
    parser.add_argument(
        "--allocate", action="store_true"
    )
    parser.add_argument(
        "--check", action="store_true"
    )
    args = parser.parse_args()
    source = Path(args.tags)
    if args.output:
        if Path(args.output).resolve() == (
            source.resolve()
        ):
            parser.error(
                "Output overwrites source"
            )
    # Keep the lock across replacements.
    lock = source.with_name(".registry.lock")
    with lock.open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        rows = verified(
            source,
            Path(args.history),
            Path(args.root),
        )
        if args.check:
            print(
                "Registry history verified"
            )
            return
        result = render(
            rows,
            labels_in(args.texfile),
            allocate=args.allocate,
        )
        text = serialize(result)
        if args.allocate:
            record(
                source,
                Path(args.history),
                Path(args.root),
                result,
            )
        if args.output:
            atomic_write(args.output, text)
        elif not args.allocate:
            print(text, end="")


if __name__ == "__main__":
    try:
        main()
    except (RegistryError, OSError) as error:
        raise SystemExit(str(error))
