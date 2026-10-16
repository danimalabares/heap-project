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

    def seed(self, text):
        self.source.write_text(text)
        snap = self.root / "baseline.tags"
        snap.write_text(text)
        digest = hashlib.sha256(
            snap.read_bytes()
        ).hexdigest()
        entry = {
            "path": snap.name,
            "sha256": digest,
        }
        self.history.write_text(
            json.dumps(
                {
                    "version": 1,
                    "snapshots": [entry],
                }
            )
        )

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
                rows, labels, True
            )
            self.assertEqual(
                rows["0000"],
                ("alpha", False),
            )
        rows = r.render(
            rows, ["alpha", "gamma"], True
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
        for _ in range(3):
            rows = r.render(rows, [], True)
        rows = r.render(rows, ["new"], True)
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
        self.history.write_text(
            '{"version":1,"snapshots":[]}'
        )
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

    def test_conflicting_evidence_blocks(
        self,
    ):
        snap = self.root / "other.tags"
        snap.write_text("0000,different\n")
        manifest = json.loads(
            self.history.read_text()
        )
        manifest["snapshots"].append(
            {
                "path": "baseline.tags",
                "sha256": hashlib.sha256(
                    snap.read_bytes()
                ).hexdigest(),
            }
        )
        self.history.write_text(
            json.dumps(manifest)
        )
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
        del rows["0002"]
        self.source.write_text(
            r.serialize(rows)
        )
        with self.assertRaises(
            r.RegistryError
        ):
            self.verified()

    def test_interrupted_allocation_blocks(
        self,
    ):
        rows = r.render(
            self.verified(), ["new"], True
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
                    self.root,
                    rows,
                )
        with self.assertRaises(
            r.RegistryError
        ):
            self.verified()

    def test_unrecorded_mapping_fails(self):
        with self.source.open("a") as stream:
            stream.write("0002,unrecorded\n")
        with self.assertRaises(
            r.RegistryError
        ):
            self.verified()


if __name__ == "__main__":
    unittest.main()
