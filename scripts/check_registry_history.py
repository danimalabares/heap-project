"""Check registry changes against Git."""

import argparse
import json
import subprocess

from gerby_registry import (
    ROOT,
    RegistryError,
    number,
    parse,
    preserve,
    read,
    read_json,
    read_migrations,
)


def git_file(root, base, path):
    return subprocess.check_output(
        ["git", "show", base + ":" + path],
        cwd=root,
        stderr=subprocess.DEVNULL,
    )


def git_files(root, base, directory):
    return subprocess.check_output(
        [
            "git",
            "ls-tree",
            "--name-only",
            base,
            directory + "/",
        ],
        cwd=root,
        text=True,
    ).split()


def check(base, root=ROOT):
    """Merged history is append-only."""
    migrations = read_migrations(
        root
        / "scripts"
        / "gerby_label_migrations.json"
    )
    try:
        old = git_file(
            root, base, "registry/tags"
        )
    except subprocess.CalledProcessError:
        old = git_file(
            root, base, "gerby/tags"
        )
    preserve(
        parse(old.decode(), migrations),
        read(
            root / "registry/tags",
            migrations,
        ),
    )
    current = read_json(
        root / "registry/history.json"
    )
    try:
        manifest = json.loads(
            git_file(
                root,
                base,
                "registry/history.json",
            )
        )
    except subprocess.CalledProcessError:
        # Retain the first repair input.
        if not any(
            (root / s["path"]).read_bytes()
            == old
            for s in current["snapshots"]
        ):
            raise RegistryError(
                "Missing original evidence"
            )
        return
    if number(
        current["allocation_floor"]
    ) < number(
        manifest.get(
            "allocation_floor", "0000"
        )
    ):
        raise RegistryError(
            "Lowered allocation floor"
        )
    paths = {
        s["path"]: s
        for s in current["snapshots"]
    }
    for snapshot in manifest["snapshots"]:
        new = paths.get(snapshot["path"])
        if new is None or any(
            new.get(key) != snapshot.get(key)
            for key in ("sha256", "role")
        ):
            raise RegistryError(
                "Changed historical snapshot: "
                + snapshot["path"]
            )
    paths = [
        s["path"] for s in manifest["snapshots"]
    ] + git_files(
        root, base, "registry/snapshots"
    )
    for path in paths:
        file = root / path
        if (
            not file.exists()
            or git_file(root, base, path)
            != file.read_bytes()
        ):
            raise RegistryError(
                "Changed historical snapshot: "
                + path
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base", required=True
    )
    check(parser.parse_args().base)
    print("No prior assignments discarded")
