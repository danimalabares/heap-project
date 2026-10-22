"""Reconstruct a historical build locally.

Outputs are inferred, never live backups.
Runs the build scripts from the given commit.
Use only reviewed Heap Project revisions.
"""

import argparse
import hashlib
import io
import json
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def reconstruct(commit):
    def git(*args):
        return subprocess.check_output(
            ["git", *args], cwd=ROOT
        )

    names = (
        git("ls-tree", "--name-only", commit)
        .decode()
        .splitlines()
    )
    paths = [
        n
        for n in names
        if (
            n.endswith(".tex")
            or n
            in {
                "scripts",
                "Makefile",
                "order-chapters.txt",
            }
        )
    ]
    paths.append("gerby/tags")
    data = git(
        "archive", commit, "--", *paths
    )
    with tempfile.TemporaryDirectory() as td:
        root = Path(td).resolve()
        with tarfile.open(
            fileobj=io.BytesIO(data)
        ) as archive:
            # Only regular files inside root.
            for (
                member
            ) in archive.getmembers():
                path = (
                    root / member.name
                ).resolve()
                if not path.is_relative_to(
                    root
                ):
                    raise ValueError(
                        "Unsafe archive"
                    )
                if not (
                    member.isfile()
                    or member.isdir()
                ):
                    raise ValueError(
                        "Unsafe member"
                    )
            archive.extractall(td)
        make = (
            root / "Makefile"
        ).read_text()
        make = make.replace("\\\n", " ")
        files = (
            re.search(
                r"^GERBY_FILES\s*\??="
                r"\s*(.*)$",
                make,
                re.M,
            )
            .group(1)
            .split()
        )
        order = re.search(
            r"^GERBY_ORDER\s*\??=\s*(.*)$",
            make,
            re.M,
        )
        command = [
            "python3",
            "scripts/make_gerby_book.py",
        ]
        if order:
            command += [
                "--order",
                order.group(1),
            ]
        book = subprocess.check_output(
            command + files, cwd=root
        )
        (
            root / "gerby/book.tex"
        ).write_bytes(book)
        tags = subprocess.check_output(
            [
                "python3",
                "scripts/gerby_tagger.py",
                "gerby/book.tex",
                "--tags",
                "gerby/tags",
            ],
            cwd=root,
        )
    lines = tags.decode().splitlines()
    mapping = dict(
        line.lstrip("#").split(",", 1)
        for line in lines
        if line
    )
    return {
        "commit": commit,
        "book_sha256": hashlib.sha256(
            book
        ).hexdigest(),
        "registry_sha256": hashlib.sha256(
            tags
        ).hexdigest(),
        "targets": {
            t: mapping.get(t)
            for t in ["09DN", "09DP", "09DR"]
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("commit")
    args = parser.parse_args()
    print(
        json.dumps(
            reconstruct(args.commit),
            indent=2,
        )
    )
