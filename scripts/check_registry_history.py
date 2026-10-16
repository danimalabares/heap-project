"""Check registry changes against Git."""

import argparse
import json
import subprocess
from pathlib import Path

from gerby_registry import (
    ROOT,
    SOURCE,
    RegistryError,
    parse,
    preserve,
    read,
    read_migrations,
)


def git_file(base, path):
    return subprocess.check_output(
        ["git", "show", base + ":" + path],
        cwd=ROOT,
        stderr=subprocess.DEVNULL,
    )


def check(base):
    migrations = read_migrations()
    try:
        old = git_file(base, "registry/tags")
    except subprocess.CalledProcessError:
        old = git_file(base, "gerby/tags")
    preserve(
        parse(old.decode(), migrations),
        read(SOURCE, migrations),
    )
    try:
        old_manifest = git_file(
            base, "registry/history.json"
        )
    except subprocess.CalledProcessError:
        # Retain the first repair input.
        manifest = json.loads(
            (
                ROOT
                / "registry/history.json"
            ).read_text()
        )
        if not any(
            (ROOT / s["path"]).read_bytes()
            == old
            for s in manifest["snapshots"]
        ):
            raise RegistryError(
                "Missing original evidence"
            )
        return
    manifest = json.loads(old_manifest)
    current = json.loads(
        (
            ROOT / "registry/history.json"
        ).read_text()
    )
    for snapshot in manifest["snapshots"]:
        if (
            snapshot
            not in current["snapshots"]
        ):
            raise RegistryError(
                "Removed historical snapshot"
            )
        path = snapshot["path"]
        if (
            git_file(base, path)
            != (ROOT / path).read_bytes()
        ):
            raise RegistryError(
                "Changed historical snapshot"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base", required=True
    )
    check(parser.parse_args().base)
    print("No prior assignments discarded")
