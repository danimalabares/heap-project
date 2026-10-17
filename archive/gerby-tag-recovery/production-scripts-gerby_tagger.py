#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


CHARACTERS = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"


def tobase(i):
    if i < len(CHARACTERS):
        return CHARACTERS[i]
    return tobase(i // len(CHARACTERS)) + CHARACTERS[i % len(CHARACTERS)]


def totag(i):
    return tobase(i).rjust(4, "0")


def toint(tag):
    return sum(
        CHARACTERS.index(tag[i]) * len(CHARACTERS) ** (4 - i - 1)
        for i in range(4)
    )


def existing_tags(path):
    migration_path = Path(__file__).with_name("gerby_label_migrations.json")
    migrations = json.loads(migration_path.read_text()) if migration_path.exists() else {}
    tags = {}
    labels = {}
    inactive = []
    if not path.exists():
        return tags, labels, inactive

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        if line.startswith("#"):
            pieces = line[1:].split(",", 1)
            if len(pieces) == 2 and len(pieces[0]) == 4:
                inactive.append(pieces[0])
            continue
        tag, label = line.split(",", 1)
        label = migrations.get(label, label)
        tags[tag] = label
        labels[label] = tag
    return tags, labels, inactive


def labels_in(path):
    text = path.read_text(encoding="utf-8")
    return re.findall(r"\\label\{([^}]*)\}", text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("texfile", default="gerby/book.tex", nargs="?")
    parser.add_argument("--tags", default="gerby/tags")
    args = parser.parse_args()

    tags_path = Path(args.tags)
    tags, labels, inactive = existing_tags(tags_path)
    try:
        current = toint(sorted(list(tags.keys()) + inactive)[-1]) + 1
    except IndexError:
        current = 0

    seen = set()
    emitted = set()
    for label in labels_in(Path(args.texfile)):
        if label in seen:
            continue
        seen.add(label)
        if label not in labels:
            tag = totag(current)
            current += 1
        else:
            tag = labels[label]
        emitted.add(tag)
        print(f"{tag},{label}")

    for tag, label in sorted(tags.items()):
        if tag not in emitted:
            print(f"#{tag},{label}")


if __name__ == "__main__":
    main()
