#!/usr/bin/env python3
"""Compare a live registry with a build.

Fails if any live assignment is missing
or bound to another label. Reports live
tags that the candidate retires and tags
that it newly serves.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

from gerby_registry import (
    ROOT,
    RegistryError,
    parse,
    read,
    read_migrations,
)

RECOVERED = (
    ROOT
    / "archive/gerby-tag-recovery"
    / "production-20261016.json"
)


def compare(live, candidate):
    lost = []
    changed = []
    retired = []
    for tag, (label, active) in sorted(
        live.items()
    ):
        if tag not in candidate:
            lost.append(tag)
        elif candidate[tag][0] != label:
            changed.append(tag)
        elif active and not candidate[tag][1]:
            retired.append(tag)
    added = sorted(
        tag
        for tag, (_, active) in candidate.items()
        if active
        and not live.get(tag, ("", False))[1]
    )
    return lost, changed, retired, added


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("live")
    parser.add_argument(
        "--candidate",
        default=str(ROOT / "gerby" / "tags"),
    )
    args = parser.parse_args()
    data = Path(args.live).read_bytes()
    migrations = read_migrations()
    # Production files predate the migrations.
    live = parse(
        data.decode(),
        migrations,
        unique_labels=False,
    )
    candidate = read(
        args.candidate, migrations
    )
    lost, changed, retired, added = compare(
        live, candidate
    )
    digest = hashlib.sha256(data).hexdigest()
    recovered = json.loads(
        RECOVERED.read_text()
    )["sha256"]
    active = sum(a for _, a in live.values())
    print(f"Live: {len(live)} tags, {active} active")
    print(
        "Live checksum "
        + (
            "matches"
            if digest == recovered
            else "DIFFERS from"
        )
        + " the 2026-10-16 recovery"
    )
    for name, tags in [
        ("Lost", lost),
        ("Reassigned", changed),
        ("Retired by source changes", retired),
        ("Newly served", added),
    ]:
        print(f"{name}: {len(tags)}")
        for tag in tags:
            label = (candidate.get(tag) or live[tag])[0]
            print(f"  {tag} {label}")
    if lost or changed:
        raise RegistryError(
            "Live assignments not preserved"
        )
    if digest != recovered:
        raise RegistryError(
            "Production changed: archive the new "
            "live file as canonical evidence first"
        )


if __name__ == "__main__":
    try:
        main()
    except (RegistryError, OSError) as error:
        sys.exit(str(error))
