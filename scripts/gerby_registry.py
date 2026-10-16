"""Strict permanent tag registry."""

import hashlib
import json
import os
import re
import sqlite3
import tempfile
from pathlib import Path

CHARS = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "registry" / "tags"
HISTORY = ROOT / "registry" / "history.json"
MIGRATIONS = (
    ROOT
    / "scripts"
    / "gerby_label_migrations.json"
)


class RegistryError(ValueError):
    pass


def number(tag):
    if len(tag) != 4 or any(
        c not in CHARS for c in tag
    ):
        raise RegistryError(
            "Invalid tag: " + tag
        )
    value = 0
    for char in tag:
        value = value * len(CHARS)
        value += CHARS.index(char)
    return value


def tag_for(value):
    if not 0 <= value < len(CHARS) ** 4:
        raise RegistryError(
            "Tag space exhausted"
        )
    result = ""
    for _ in range(4):
        value, digit = divmod(
            value, len(CHARS)
        )
        result = CHARS[digit] + result
    return result


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise RegistryError(
                    "Duplicate JSON key: "
                    + key
                )
            result[key] = value
        return result

    return json.loads(
        Path(path).read_text(),
        object_pairs_hook=unique,
    )


def canonical(label, migrations):
    seen = set()
    while label in migrations:
        if label in seen:
            raise RegistryError(
                "Migration cycle: " + label
            )
        seen.add(label)
        label = migrations[label]
    return label


def read_migrations(path=MIGRATIONS):
    result = read_json(path)
    if not isinstance(result, dict):
        raise RegistryError(
            "Invalid migrations"
        )
    for old, new in result.items():
        if (
            not isinstance(new, str)
            or not new
        ):
            raise RegistryError(
                "Invalid migration: " + old
            )
        canonical(old, result)
    return result


def parse(
    text,
    migrations=None,
    unique_labels=True,
    legacy=False,
):
    migrations = migrations or {}
    rows = {}
    labels = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        active = not line.startswith("#")
        row = line if active else line[1:]
        # Read legacy tombstone columns.
        # Preserve the original identity.
        if legacy and not active:
            pieces = row.split(",")
            if len(pieces) == 3:
                number(pieces[2])
                row = ",".join(pieces[:2])
        if row.count(",") != 1:
            raise RegistryError(
                "Malformed registry row: "
                + line
            )
        tag, label = row.split(",")
        number(tag)
        if not re.fullmatch(
            r"[A-Za-z0-9:-]+", label
        ):
            raise RegistryError(
                "Invalid label: " + label
            )
        label = canonical(label, migrations)
        if tag in rows:
            raise RegistryError(
                "Duplicate tag: " + tag
            )
        if unique_labels and label in labels:
            raise RegistryError(
                "Duplicate label: " + label
            )
        rows[tag] = (label, active)
        labels[label] = tag
    if not rows:
        raise RegistryError("Empty registry")
    return rows


def read(path, migrations=None):
    return parse(
        Path(path).read_text(), migrations
    )


def serialize(rows):
    return "".join(
        ("" if active else "#")
        + tag
        + ","
        + label
        + "\n"
        for tag, (label, active) in sorted(
            rows.items()
        )
    )


def preserve(previous, current):
    for tag, (label, _) in previous.items():
        if tag not in current:
            raise RegistryError(
                "Lost historical tag: " + tag
            )
        if current[tag][0] != label:
            raise RegistryError(
                "Reassigned tag: " + tag
            )


def history_issues(
    rows, history, root, migrations
):
    manifest = read_json(history)
    if manifest.get("version") != 1:
        raise RegistryError(
            "Unknown history format"
        )
    if not manifest.get("snapshots"):
        raise RegistryError(
            "Missing registry history"
        )
    observed = {}
    for snapshot in manifest["snapshots"]:
        path = root / snapshot["path"]
        data = path.read_bytes()
        digest = hashlib.sha256(
            data
        ).hexdigest()
        if digest != snapshot["sha256"]:
            raise RegistryError(
                "History checksum mismatch: "
                + snapshot["path"]
            )
        old = parse(
            data.decode(),
            migrations,
            unique_labels=False,
            legacy=True,
        )
        for tag, (label, _) in old.items():
            observed.setdefault(tag, set())
            observed[tag].add(label)
    conflicts = {
        t: sorted(labels)
        for t, labels in observed.items()
        if len(labels) > 1
    }
    missing = sorted(
        observed.keys() - rows.keys()
    )
    changed = sorted(
        t
        for t, (label, _) in rows.items()
        if label
        not in observed.get(t, set())
    )
    return {
        "conflicts": conflicts,
        "missing": missing,
        "changed": changed,
    }


def verified(
    source=SOURCE,
    history=HISTORY,
    root=ROOT,
    migrations=None,
):
    if migrations is None:
        migrations = read_migrations()
    rows = read(source, migrations)
    issues = history_issues(
        rows, history, root, migrations
    )
    if any(issues.values()):
        counts = ", ".join(
            f"{key}={len(value)}"
            for key, value in issues.items()
        )
        raise RegistryError(
            "Unreconciled registry history: "
            + counts
        )
    return rows


def labels_in(path):
    text = Path(path).read_text()
    # Ignore labels inside TeX comments.
    text = re.sub(
        r"(?<!\\)%[^\n]*", "", text
    )
    labels = re.findall(
        r"\\label\{([^}]*)\}", text
    )
    if len(labels) != len(set(labels)):
        raise RegistryError(
            "Duplicate source label"
        )
    return labels


def render(rows, labels, allocate=False):
    if len(labels) != len(set(labels)):
        raise RegistryError(
            "Duplicate source label"
        )
    lookup = {
        label: tag
        for tag, (label, _) in rows.items()
    }
    missing = [
        l for l in labels if l not in lookup
    ]
    if missing and not allocate:
        raise RegistryError(
            "Unregistered source labels: "
            + ", ".join(missing[:5])
            + "; run make gerby-register"
        )
    current = max(map(number, rows)) + 1
    result = {
        t: (l, False)
        for t, (l, _) in rows.items()
    }
    for label in labels:
        if label not in lookup:
            lookup[label] = tag_for(current)
            current += 1
        result[lookup[label]] = (label, True)
    # Validate before writing any output.
    return parse(serialize(result))


def atomic_write(path, text):
    path = Path(path)
    fd, temporary = tempfile.mkstemp(
        dir=path.parent,
        prefix="." + path.name,
    )
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def record(source, history, root, rows):
    """Persist history before source."""
    text = serialize(rows)
    data = text.encode()
    digest = hashlib.sha256(data).hexdigest()
    history = Path(history)
    directory = history.parent / "snapshots"
    snapshot = directory / (digest + ".tags")
    relative = (
        snapshot.resolve().relative_to(
            Path(root).resolve()
        )
    )
    manifest = read_json(history)
    entry = {
        "path": str(relative),
        "sha256": digest,
    }
    directory.mkdir(exist_ok=True)
    try:
        with snapshot.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        if snapshot.read_bytes() != data:
            raise RegistryError(
                "Allocation snapshot changed"
            )
    if entry not in manifest["snapshots"]:
        manifest["snapshots"].append(entry)
        atomic_write(
            history,
            json.dumps(manifest, indent=2)
            + "\n",
        )
    # Interrupted writes block later builds.
    # history already reserves the new IDs.
    atomic_write(source, text)


def check_rendered(rows, directory):
    found = set()
    for path in Path(directory).glob(
        "*.tag"
    ):
        pieces = path.stem.split("-", 3)
        if len(pieces) != 4:
            raise RegistryError(
                "Invalid tag filename"
            )
        tag, label = pieces[2:]
        if tag in found:
            raise RegistryError(
                "Duplicate rendered tag: "
                + tag
            )
        found.add(tag)
        if rows.get(tag) != (label, True):
            raise RegistryError(
                "Rendered mismatch: " + tag
            )
    if not found:
        raise RegistryError(
            "Missing rendered tags"
        )
    return found


def check_database(
    rows,
    path,
    migrations=None,
    active_tags=None,
):
    path = Path(path)
    if not path.exists():
        raise RegistryError(
            "Missing tag database"
        )
    uri = (
        path.resolve().as_uri() + "?mode=ro"
    )
    with sqlite3.connect(
        uri, uri=True
    ) as db:
        for tag, label in db.execute(
            "SELECT tag, label FROM tag"
        ):
            label = canonical(
                label, migrations or {}
            )
            if tag not in rows:
                raise RegistryError(
                    "Unknown database tag: "
                    + tag
                )
            if rows[tag][0] != label:
                raise RegistryError(
                    "Database mismatch: "
                    + tag
                )
        if active_tags is not None:
            actual = {
                tag
                for tag, in db.execute(
                    "SELECT tag FROM tag "
                    "WHERE active = 1"
                )
            }
            if actual != active_tags:
                raise RegistryError(
                    "Stale database tags"
                )


def check_runtime(root=ROOT):
    rows = verified(
        root / "registry/tags",
        root / "registry/history.json",
        root=root,
    )
    output = read(root / "gerby" / "tags")
    expected = render(
        rows,
        labels_in(root / "gerby/book.tex"),
    )
    if output != expected:
        raise RegistryError(
            "Stale rendered registry"
        )
    active = check_rendered(
        output, root / "gerby/document"
    )
    check_database(
        output,
        root / "gerby/stack.sqlite",
        active_tags=active,
    )
