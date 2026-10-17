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
ROLES = ("legacy", "canonical")
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


def checked_bytes(path, digest):
    data = Path(path).read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != digest:
        raise RegistryError(
            "History checksum mismatch: "
            + str(path)
        )
    return data


class Evidence:
    """Checksummed registry history.

    Legacy snapshots are frozen pre-repair
    observations. They may contradict each
    other; their IDs are only reserved.
    Canonical snapshots and allocation
    deltas define registry/tags exactly.
    """

    def __init__(self, history, root, migrations):
        manifest = read_json(history)
        if manifest.get("version") != 2:
            raise RegistryError(
                "Unknown history format"
            )
        if not manifest.get("snapshots"):
            raise RegistryError(
                "Missing registry history"
            )
        self.floor = number(
            manifest["allocation_floor"]
        )
        # (source, role, rows)
        self.snapshots = []
        for entry in manifest["snapshots"]:
            role = entry.get("role")
            if role not in ROLES:
                raise RegistryError(
                    "Unknown snapshot role: "
                    + entry["path"]
                )
            data = checked_bytes(
                Path(root) / entry["path"],
                entry["sha256"],
            )
            rows = parse(
                data.decode(),
                migrations,
                unique_labels=False,
                legacy=role == "legacy",
            )
            self.snapshots.append(
                (
                    entry.get(
                        "description",
                        entry["path"],
                    ),
                    role,
                    rows,
                )
            )
        if not any(
            role == "canonical"
            for _, role, _ in self.snapshots
        ):
            raise RegistryError(
                "Missing canonical history"
            )
        # Deltas are named by their checksum.
        directory = (
            Path(history).parent / "snapshots"
        )
        for path in sorted(
            directory.glob("*.tags")
        ):
            data = checked_bytes(
                path, path.stem
            )
            self.snapshots.append(
                (
                    "allocation "
                    + path.stem[:12],
                    "allocation",
                    parse(
                        data.decode(),
                        migrations,
                    ),
                )
            )
        # Deterministic replays of old builds.
        self.builds = []
        for entry in manifest.get(
            "observations", []
        ):
            data = checked_bytes(
                Path(root) / entry["path"],
                entry["sha256"],
            )
            for build in json.loads(data):
                targets = {}
                for tag, label in build[
                    "targets"
                ].items():
                    number(tag)
                    if label:
                        targets[tag] = canonical(
                            label, migrations
                        )
                self.builds.append(
                    (
                        "reconstructed build "
                        + build["commit"][:9]
                        + " ("
                        + build["date"][:10]
                        + ")",
                        targets,
                    )
                )
        self.observed = {}
        for source, role, rows in self.snapshots:
            for tag, (label, _) in rows.items():
                self.observed.setdefault(
                    tag, []
                ).append((label, source, role))
        for source, targets in self.builds:
            for tag, label in targets.items():
                self.observed.setdefault(
                    tag, []
                ).append(
                    (
                        label,
                        source,
                        "reconstructed",
                    )
                )

    def historical(self):
        """Labels observed before allocation."""
        result = {}
        for tag, items in self.observed.items():
            labels = {
                label
                for label, _, role in items
                if role != "allocation"
            }
            if labels:
                result[tag] = labels
        return result

    def canonical(self):
        result = {}
        for _, role, rows in self.snapshots:
            if role == "legacy":
                continue
            for tag, (label, _) in rows.items():
                if (
                    result.setdefault(tag, label)
                    != label
                ):
                    raise RegistryError(
                        "Conflicting canonical "
                        "tag: " + tag
                    )
        return result

    def check_allocations(self):
        historical = self.historical()
        for _, role, rows in self.snapshots:
            if role != "allocation":
                continue
            for tag, (label, _) in rows.items():
                known = historical.get(tag)
                # Recovering an identity is fine.
                if known == {label}:
                    continue
                if (
                    known
                    or number(tag) < self.floor
                ):
                    raise RegistryError(
                        "Allocation reuses "
                        "historical tag: " + tag
                    )

    def next_number(self, rows):
        used = set(rows) | set(self.observed)
        return max(
            self.floor,
            max(map(number, used)) + 1,
        )


def check(
    source=SOURCE,
    history=HISTORY,
    root=ROOT,
    migrations=None,
    restore=False,
):
    """Return verified rows and evidence.

    registry/tags must map exactly the tags
    of canonical and allocation snapshots.
    With restore, canonical rows missing
    after an interrupted allocation are
    reinstated as tombstones.
    """
    if migrations is None:
        migrations = read_migrations()
    rows = read(source, migrations)
    evidence = Evidence(
        history, root, migrations
    )
    evidence.check_allocations()
    expected = evidence.canonical()
    for tag, label in expected.items():
        if tag not in rows and restore:
            rows[tag] = (label, False)
        elif tag not in rows:
            raise RegistryError(
                "Lost historical tag: " + tag
            )
        elif rows[tag][0] != label:
            raise RegistryError(
                "Reassigned tag: " + tag
            )
    unrecorded = sorted(
        rows.keys() - expected.keys()
    )
    if unrecorded:
        raise RegistryError(
            "Unrecorded assignment: "
            + unrecorded[0]
        )
    return parse(serialize(rows)), evidence


def verified(
    source=SOURCE,
    history=HISTORY,
    root=ROOT,
    migrations=None,
):
    return check(
        source, history, root, migrations
    )[0]


def summary(rows, evidence):
    historical = evidence.historical()
    reserved = historical.keys() - rows.keys()
    conflicts = [
        tag
        for tag, labels in historical.items()
        if len(labels) > 1
    ]
    active = sum(a for _, a in rows.values())
    return (
        f"Registry verified: {len(rows)} "
        f"assignments, {active} active.\n"
        f"Historical IDs: {len(historical)}; "
        f"{len(conflicts)} conflicting; "
        f"{len(reserved)} reserved outside "
        f"the registry.\n"
        f"Allocation floor "
        f"{tag_for(evidence.floor)}; next "
        f"{tag_for(evidence.next_number(rows))}."
    )


def provenance(tag, rows, evidence):
    """Describe what is known about a tag."""
    tag = tag.upper()
    try:
        value = number(tag)
    except RegistryError:
        return {"tag": tag, "status": "invalid"}
    items = evidence.observed.get(tag, [])
    labels = {}
    for label, source, role in items:
        labels.setdefault(label, []).append(
            (source, role)
        )
    current = rows.get(tag)
    if current:
        status = (
            "active" if current[1] else "retired"
        )
    elif len(labels) == 1:
        status = "historical"
    elif labels:
        status = "ambiguous"
    elif value < evidence.floor:
        status = "reserved"
    else:
        status = "unknown"
    location = {
        label: other
        for other, (label, active) in rows.items()
        if active
    }
    return {
        "tag": tag,
        "status": status,
        "label": current[0] if current else None,
        "conflicting": bool(
            set(labels) - {current[0]}
            if current
            else len(labels) > 1
        ),
        "evidence": [
            {
                "label": label,
                "current": location.get(label),
                "sources": sources,
            }
            for label, sources in sorted(
                labels.items()
            )
        ],
    }


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


def render(
    rows, labels, allocate=False, evidence=None
):
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
    result = {
        t: (l, False)
        for t, (l, _) in rows.items()
    }
    recover = {}
    if missing:
        if evidence is None:
            raise RegistryError(
                "Allocation needs history"
            )
        current = evidence.next_number(rows)
        # Unambiguous retired identities.
        for tag, known in (
            evidence.historical().items()
        ):
            if tag not in rows and len(known) == 1:
                recover.setdefault(
                    next(iter(known)), []
                ).append(tag)
    for label in labels:
        if label not in lookup:
            old = recover.get(label, [])
            if len(old) == 1:
                lookup[label] = old[0]
            else:
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


def record(source, history, rows, previous):
    """Persist new tags before the source."""
    added = {
        tag: row
        for tag, row in rows.items()
        if tag not in previous
    }
    if added:
        data = serialize(added).encode()
        digest = hashlib.sha256(
            data
        ).hexdigest()
        directory = (
            Path(history).parent / "snapshots"
        )
        directory.mkdir(exist_ok=True)
        snapshot = directory / (
            digest + ".tags"
        )
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
    # An interruption here leaves a delta
    # without source rows. Builds then fail;
    # make gerby-register restores them.
    atomic_write(source, serialize(rows))
    return added


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
