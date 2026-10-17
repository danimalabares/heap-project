"""Permanent tag regression fixtures."""

import hashlib
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import gerby_registry as r


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = (
            tempfile.TemporaryDirectory()
        )
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "tags"
        self.history = (
            self.root / "history.json"
        )
        self.tex = self.root / "book.tex"
        self.output = self.root / "rendered"
        self.seed("0000,alpha\n0001,beta\n")

    def seed(
        self, text, legacy=(), floor="0000"
    ):
        self.source.write_text(text)
        snapshots = []
        for name, role, data in [
            ("baseline.tags", "canonical", text)
        ] + [
            (f"legacy{i}.tags", "legacy", data)
            for i, data in enumerate(legacy)
        ]:
            snap = self.root / name
            snap.write_text(data)
            snapshots.append(
                {
                    "path": name,
                    "sha256": hashlib.sha256(
                        snap.read_bytes()
                    ).hexdigest(),
                    "role": role,
                }
            )
        self.history.write_text(
            json.dumps(
                {
                    "version": 2,
                    "allocation_floor": floor,
                    "snapshots": snapshots,
                }
            )
        )

    def evidence(self):
        return r.Evidence(
            self.history, self.root, {}
        )

    def delta(self, text):
        directory = self.root / "snapshots"
        directory.mkdir(exist_ok=True)
        digest = hashlib.sha256(
            text.encode()
        ).hexdigest()
        path = directory / (digest + ".tags")
        path.write_text(text)
        return path

    def verified(self):
        return r.verified(
            self.source,
            self.history,
            self.root,
            {},
        )

    def cli(self, labels, *extra):
        self.tex.write_text(
            "".join(
                "\\label{" + l + "}\n"
                for l in labels
            )
        )
        script = Path(__file__).with_name(
            "gerby_tagger.py"
        )
        return subprocess.run(
            [
                sys.executable,
                str(script),
                str(self.tex),
                "--tags",
                str(self.source),
                "--history",
                str(self.history),
                "--root",
                str(self.root),
                *extra,
            ],
            capture_output=True,
            text=True,
        )

    def test_restore_after_many_builds(
        self,
    ):
        rows = self.verified()
        for labels in [
            ["beta"],
            ["beta", "gamma"],
            ["beta", "gamma"],
        ]:
            rows = r.render(
                rows,
                labels,
                True,
                self.evidence(),
            )
            self.assertEqual(
                rows["0000"],
                ("alpha", False),
            )
        rows = r.render(
            rows,
            ["alpha", "gamma"],
            True,
            self.evidence(),
        )
        self.assertEqual(
            rows["0000"], ("alpha", True)
        )
        self.assertEqual(
            rows["0002"][0], "gamma"
        )

    def test_highest_tombstone(
        self,
    ):
        rows = r.parse("#000Z,old\n")
        evidence = self.evidence()
        for _ in range(3):
            rows = r.render(
                rows, [], True, evidence
            )
        rows = r.render(
            rows, ["new"], True, evidence
        )
        self.assertIn("0010", rows)
        self.assertEqual(
            rows["000Z"][0], "old"
        )

    def test_empty_or_missing_registry_fails(
        self,
    ):
        for text in ["", "\n"]:
            with self.assertRaises(
                r.RegistryError
            ):
                r.parse(text)
        self.source.unlink()
        with self.assertRaises(
            FileNotFoundError
        ):
            self.verified()

    def test_bad_rows_fail(self):
        for text in [
            "000I,a",
            "000O,a",
            "00000,a",
            "000a,a",
            "0000,",
            "#comment",
            "0000,a,b",
            "0000,a b",
            "#0000,a,0001",
        ]:
            with self.subTest(text=text):
                with self.assertRaises(
                    r.RegistryError
                ):
                    r.parse(text)

    def test_duplicates_active_and_inactive(
        self,
    ):
        for a in ["", "#"]:
            for b in ["", "#"]:
                for second in [
                    "0000,b",
                    "0001,a",
                    "0000,a",
                ]:
                    text = (
                        a
                        + "0000,a\n"
                        + b
                        + second
                        + "\n"
                    )
                    with self.assertRaises(
                        r.RegistryError
                    ):
                        r.parse(text)

    def test_migration_chains(self):
        rows = r.parse(
            "#0000,a\n", {"a": "b", "b": "c"}
        )
        self.assertEqual(
            r.render(rows, ["c"])["0000"],
            ("c", True),
        )

    def test_migration_collisions_and_cycles(
        self,
    ):
        with self.assertRaises(
            r.RegistryError
        ):
            r.parse(
                "0000,a\n#0001,b\n",
                {"a": "b"},
            )
        with self.assertRaises(
            r.RegistryError
        ):
            r.canonical(
                "a", {"a": "b", "b": "a"}
            )

    def test_json_duplicate_keys(self):
        self.history.write_text(
            '{"a":1,"a":2}'
        )
        with self.assertRaises(
            r.RegistryError
        ):
            r.read_json(self.history)

    def test_missing_or_bad_history(
        self,
    ):
        baseline = (
            self.root / "baseline.tags"
        )
        baseline.write_text("0000,changed\n")
        with self.assertRaises(
            r.RegistryError
        ):
            self.verified()
        baseline.unlink()
        with self.assertRaises(
            FileNotFoundError
        ):
            self.verified()
        for text in [
            '{"version":1,"snapshots":[]}',
            '{"version":2,'
            '"allocation_floor":"0000",'
            '"snapshots":[]}',
        ]:
            self.history.write_text(text)
            with self.assertRaises(
                r.RegistryError
            ):
                self.verified()

    def test_lost_or_changed_identity(
        self,
    ):
        for text in [
            "0000,alpha\n",
            "0000,wrong\n0001,beta\n",
        ]:
            self.source.write_text(text)
            with self.assertRaises(
                r.RegistryError
            ):
                self.verified()

    def test_conflicting_canonical_blocks(
        self,
    ):
        manifest = json.loads(
            self.history.read_text()
        )
        other = self.root / "other.tags"
        other.write_text("0000,different\n")
        manifest["snapshots"].append(
            {
                "path": "other.tags",
                "sha256": hashlib.sha256(
                    other.read_bytes()
                ).hexdigest(),
                "role": "canonical",
            }
        )
        self.history.write_text(
            json.dumps(manifest)
        )
        with self.assertRaisesRegex(
            r.RegistryError, "Conflicting"
        ):
            self.verified()

    def test_legacy_conflicts_are_reserved(
        self,
    ):
        self.seed(
            "0000,alpha\n0001,beta\n",
            legacy=[
                "0000,old\n0005,gone\n",
                "#0005,other\n0007,lost\n",
            ],
        )
        rows = self.verified()
        self.assertNotIn("0005", rows)
        result = self.cli(
            ["alpha", "beta", "new"],
            "--allocate",
        )
        self.assertEqual(
            result.returncode, 0, result.stderr
        )
        rows = self.verified()
        self.assertEqual(
            rows["0008"], ("new", True)
        )
        for tag in ["0002", "0005", "0007"]:
            self.assertNotIn(tag, rows)

    def test_allocation_floor(self):
        self.seed(
            "0000,alpha\n0001,beta\n",
            floor="0100",
        )
        result = self.cli(
            ["new"], "--allocate"
        )
        self.assertIn(
            "Allocated 0100 new",
            result.stdout,
        )
        rows = self.verified()
        self.assertEqual(
            rows["0100"], ("new", True)
        )
        self.assertEqual(
            rows["0000"], ("alpha", False)
        )

    def test_recover_unambiguous_identity(
        self,
    ):
        self.seed(
            "0000,alpha\n0001,beta\n",
            legacy=["0000,alpha\n0007,old\n"],
            floor="0100",
        )
        result = self.cli(
            ["alpha", "old", "new"],
            "--allocate",
        )
        self.assertEqual(
            result.returncode, 0, result.stderr
        )
        rows = self.verified()
        self.assertEqual(
            rows["0007"], ("old", True)
        )
        self.assertEqual(
            rows["0100"], ("new", True)
        )

    def test_ambiguous_identity_is_new(
        self,
    ):
        self.seed(
            "0000,alpha\n0001,beta\n",
            legacy=["0007,old\n", "0007,x\n"],
        )
        result = self.cli(
            ["old"], "--allocate"
        )
        self.assertEqual(
            result.returncode, 0, result.stderr
        )
        rows = self.verified()
        self.assertEqual(
            rows["0008"], ("old", True)
        )
        self.assertNotIn("0007", rows)

    def test_allocation_cannot_reuse_history(
        self,
    ):
        for floor, legacy, row in [
            ("0000", "0005,gone\n", "0005,new"),
            ("0100", "0000,alpha\n", "0050,new"),
        ]:
            with self.subTest(row=row):
                self.seed(
                    "0000,alpha\n0001,beta\n",
                    legacy=[legacy],
                    floor=floor,
                )
                for old in self.root.glob(
                    "snapshots/*"
                ):
                    old.unlink()
                self.delta(row + "\n")
                with self.source.open(
                    "a"
                ) as stream:
                    stream.write(row + "\n")
                with self.assertRaisesRegex(
                    r.RegistryError, "reuses"
                ):
                    self.verified()

    def test_concurrent_allocations_collide(
        self,
    ):
        before = self.source.read_text()
        first = self.cli(
            ["alpha", "beta", "one"],
            "--allocate",
        )
        self.assertEqual(
            first.returncode, 0, first.stderr
        )
        merged = self.source.read_text()
        # A second branch from the same base.
        (delta,) = self.root.glob(
            "snapshots/*.tags"
        )
        delta.unlink()
        self.source.write_text(before)
        rows = r.render(
            r.parse(before),
            ["alpha", "beta", "two"],
            True,
            r.Evidence(
                self.history, self.root, {}
            ),
        )
        self.assertEqual(
            rows["0002"][0], "two"
        )
        # Merging both branches must fail.
        self.delta("0002,one\n")
        self.delta("0002,two\n")
        for text in [
            merged,
            merged + "0002,two\n",
        ]:
            self.source.write_text(text)
            with self.assertRaises(
                r.RegistryError
            ):
                self.verified()

    def test_source_duplicate_labels_fail(
        self,
    ):
        with self.assertRaises(
            r.RegistryError
        ):
            r.render(
                self.verified(), ["a", "a"]
            )
        self.tex.write_text(
            "\\label{a}\n\\label{a}\n"
        )
        with self.assertRaises(
            r.RegistryError
        ):
            r.labels_in(self.tex)

    def test_comment_labels_ignored(self):
        self.tex.write_text(
            "% \\label{fake}\n\\label{alpha}"
        )
        self.assertEqual(
            r.labels_in(self.tex), ["alpha"]
        )

    def test_exhaustion_is_atomic(
        self,
    ):
        self.seed("ZZZZ,last\n")
        result = self.cli(
            ["new"], "--allocate"
        )
        self.assertNotEqual(
            result.returncode, 0
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            self.source.read_text(),
            "ZZZZ,last\n",
        )

    def test_build_cannot_allocate(self):
        before = self.source.read_bytes()
        result = self.cli(["alpha", "new"])
        self.assertNotEqual(
            result.returncode, 0
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            self.source.read_bytes(), before
        )

    def test_explicit_allocation_then_build(
        self,
    ):
        result = self.cli(
            ["beta", "new"], "--allocate"
        )
        self.assertEqual(
            result.returncode,
            0,
            result.stderr,
        )
        self.assertIn(
            "#0000,alpha",
            self.source.read_text(),
        )
        result = self.cli(["alpha", "new"])
        self.assertEqual(
            result.returncode,
            0,
            result.stderr,
        )
        self.assertIn(
            "0000,alpha", result.stdout
        )
        self.assertIn(
            "0002,new", result.stdout
        )

    def test_failed_output_is_unchanged(
        self,
    ):
        self.output.write_text(
            "previous output"
        )
        result = self.cli(
            ["unknown"],
            "--output",
            str(self.output),
        )
        self.assertNotEqual(
            result.returncode, 0
        )
        self.assertEqual(
            self.output.read_text(),
            "previous output",
        )

    def test_output_cannot_overwrite_source(
        self,
    ):
        before = self.source.read_bytes()
        result = self.cli(
            ["alpha"],
            "--output",
            str(self.source),
        )
        self.assertNotEqual(
            result.returncode, 0
        )
        self.assertEqual(
            before, self.source.read_bytes()
        )

    def test_atomic_failure_keeps_old_file(
        self,
    ):
        before = self.source.read_bytes()
        with patch.object(
            r.os,
            "replace",
            side_effect=OSError,
        ):
            with self.assertRaises(OSError):
                r.atomic_write(
                    self.source, "new"
                )
        self.assertEqual(
            before, self.source.read_bytes()
        )

    def test_rendered_identity_mismatch(
        self,
    ):
        file = (
            self.root
            / "lemma-1-0000-wrong.tag"
        )
        file.write_text("wrong")
        with self.assertRaises(
            r.RegistryError
        ):
            r.check_rendered(
                self.verified(), self.root
            )

    def test_database_mismatch_is_read_only(
        self,
    ):
        file = self.root / "stack.sqlite"
        with sqlite3.connect(file) as db:
            db.execute(
                "CREATE TABLE tag "
                "(tag TEXT, label TEXT)"
            )
            db.execute(
                "INSERT INTO tag "
                "VALUES(?,?)",
                ("0000", "wrong"),
            )
        before = file.read_bytes()
        with self.assertRaises(
            r.RegistryError
        ):
            r.check_database(
                self.verified(), file
            )
        self.assertEqual(
            before, file.read_bytes()
        )

    def test_preserve_checks_base_registry(
        self,
    ):
        rows = self.verified()
        for new in [
            {"0000": ("alpha", True)},
            {"0000": ("wrong", True)},
        ]:
            with self.assertRaises(
                r.RegistryError
            ):
                r.preserve(rows, new)

    def test_legacy_tombstone_evidence(self):
        rows = r.parse(
            "#0000,alpha,0001\n", legacy=True
        )
        self.assertEqual(
            rows["0000"], ("alpha", False)
        )

    def test_new_allocation_enters_history(
        self,
    ):
        result = self.cli(
            ["alpha", "new"], "--allocate"
        )
        self.assertEqual(
            result.returncode, 0
        )
        rows = self.verified()
        self.assertEqual(
            rows["0002"][0], "new"
        )
        (delta,) = self.root.glob(
            "snapshots/*.tags"
        )
        self.assertEqual(
            delta.read_text(), "0002,new\n"
        )
        text = self.source.read_text()
        del rows["0002"]
        self.source.write_text(
            r.serialize(rows)
        )
        with self.assertRaises(
            r.RegistryError
        ):
            self.verified()
        self.source.write_text(text)
        delta.unlink()
        with self.assertRaisesRegex(
            r.RegistryError, "Unrecorded"
        ):
            self.verified()

    def test_corrupt_delta_fails(self):
        self.cli(["alpha", "new"], "--allocate")
        (delta,) = self.root.glob(
            "snapshots/*.tags"
        )
        delta.write_text("0002,other\n")
        with self.assertRaisesRegex(
            r.RegistryError, "checksum"
        ):
            self.verified()

    def test_interrupted_allocation_blocks(
        self,
    ):
        rows = self.verified()
        result = r.render(
            rows, ["new"], True, self.evidence()
        )
        original = r.atomic_write

        def interrupted(path, text):
            if Path(path) == self.source:
                raise OSError("interrupted")
            original(path, text)

        with patch.object(
            r,
            "atomic_write",
            side_effect=interrupted,
        ):
            with self.assertRaises(OSError):
                r.record(
                    self.source,
                    self.history,
                    result,
                    rows,
                )
        with self.assertRaisesRegex(
            r.RegistryError, "Lost"
        ):
            self.verified()
        # Explicit allocation restores it.
        repaired = self.cli(
            ["alpha", "other"], "--allocate"
        )
        self.assertEqual(
            repaired.returncode,
            0,
            repaired.stderr,
        )
        rows = self.verified()
        self.assertEqual(
            rows["0002"], ("new", False)
        )
        self.assertEqual(
            rows["0003"], ("other", True)
        )

    def test_unrecorded_mapping_fails(self):
        with self.source.open("a") as stream:
            stream.write("0002,unrecorded\n")
        with self.assertRaises(
            r.RegistryError
        ):
            self.verified()

    def test_provenance_statuses(self):
        self.seed(
            "0000,alpha\n#0001,beta\n",
            legacy=[
                "0000,older\n0003,gone\n"
                "0004,first\n",
                "0004,second\n",
            ],
            floor="0010",
        )
        rows, evidence = r.check(
            self.source,
            self.history,
            self.root,
            {},
        )
        expected = {
            "0000": ("active", True),
            "0001": ("retired", False),
            "0003": ("historical", False),
            "0004": ("ambiguous", True),
            "0009": ("reserved", False),
            "0010": ("unknown", False),
        }
        for tag, (status, conflict) in (
            expected.items()
        ):
            info = r.provenance(
                tag, rows, evidence
            )
            self.assertEqual(
                info["status"], status, tag
            )
            self.assertEqual(
                info["conflicting"],
                conflict,
                tag,
            )
        info = r.provenance(
            "0000", rows, evidence
        )
        self.assertEqual(
            [e["label"] for e in info["evidence"]],
            ["alpha", "older"],
        )
        self.assertEqual(
            info["evidence"][0]["current"],
            "0000",
        )
        self.assertEqual(
            r.provenance("O000", rows, evidence)[
                "status"
            ],
            "invalid",
        )


class ProductionCompareTests(unittest.TestCase):
    def test_compare(self):
        from compare_production_registry import (
            compare,
        )

        live = r.parse(
            "0000,a\n0001,b\n#0002,c\n0003,d\n"
        )
        candidate = r.parse(
            "0000,a\n#0001,b\n#0002,c\n"
            "0003,d\n0100,e\n"
        )
        self.assertEqual(
            compare(live, candidate),
            ([], [], ["0001"], ["0100"]),
        )
        candidate = r.parse(
            "0000,x\n0001,b\n0003,d\n"
        )
        self.assertEqual(
            compare(live, candidate)[:2],
            (["0002"], ["0000"]),
        )


class BaseHistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = (
            tempfile.TemporaryDirectory()
        )
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "scripts").mkdir()
        (
            self.root
            / "scripts"
            / "gerby_label_migrations.json"
        ).write_text("{}")
        registry = self.root / "registry"
        (registry / "snapshots").mkdir(
            parents=True
        )
        text = "0000,alpha\n"
        (self.root / "base.tags").write_text(
            text
        )
        (registry / "tags").write_text(
            "0000,alpha\n0100,new\n"
        )
        self.delta = (
            registry
            / "snapshots"
            / "x.tags"
        )
        self.delta.write_text("0100,new\n")
        self.manifest = {
            "version": 2,
            "allocation_floor": "0100",
            "snapshots": [
                {
                    "path": "base.tags",
                    "sha256": hashlib.sha256(
                        text.encode()
                    ).hexdigest(),
                    "role": "canonical",
                }
            ],
        }
        self.write()
        for command in [
            ["init", "-q"],
            ["add", "."],
            [
                "-c",
                "user.name=t",
                "-c",
                "user.email=t@t",
                "commit",
                "-qm",
                "base",
            ],
        ]:
            subprocess.run(
                ["git", *command],
                cwd=self.root,
                check=True,
            )

    def write(self):
        (
            self.root
            / "registry"
            / "history.json"
        ).write_text(
            json.dumps(self.manifest)
        )

    def check(self):
        from check_registry_history import (
            check,
        )

        check("HEAD", self.root)

    def test_unchanged_passes(self):
        self.check()

    def test_history_is_append_only(self):
        for change in [
            lambda: self.delta.unlink(),
            lambda: self.delta.write_text("x"),
            lambda: (
                self.root / "registry/tags"
            ).write_text("0000,alpha\n"),
        ]:
            with self.subTest():
                subprocess.run(
                    ["git", "checkout", "-q", "."],
                    cwd=self.root,
                    check=True,
                )
                change()
                with self.assertRaises(
                    (r.RegistryError, OSError)
                ):
                    self.check()
        for key, value in [
            ("allocation_floor", "00ZZ"),
            ("role", "legacy"),
        ]:
            with self.subTest(key=key):
                subprocess.run(
                    ["git", "checkout", "-q", "."],
                    cwd=self.root,
                    check=True,
                )
                manifest = json.loads(
                    json.dumps(self.manifest)
                )
                if key == "role":
                    manifest["snapshots"][0][
                        key
                    ] = value
                else:
                    manifest[key] = value
                (
                    self.root
                    / "registry"
                    / "history.json"
                ).write_text(
                    json.dumps(manifest)
                )
                with self.assertRaises(
                    r.RegistryError
                ):
                    self.check()


if __name__ == "__main__":
    unittest.main()
