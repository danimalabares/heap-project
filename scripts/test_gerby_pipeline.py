"""Exercise the isolated Gerby pipeline."""

import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    def test_build_import_and_reintroduction(
        self,
    ):
        factory = tempfile.TemporaryDirectory
        with factory() as td:
            root = Path(td)
            self.root = root
            for directory in [
                "scripts",
                "gerby-website",
            ]:
                # Copy only Python source.
                source = ROOT / directory
                for file in source.rglob(
                    "*.py"
                ):
                    relative = (
                        file.relative_to(
                            ROOT
                        )
                    )
                    target = root / relative
                    target.parent.mkdir(
                        parents=True,
                        exist_ok=True,
                    )
                    shutil.copy2(
                        file, target
                    )
            for name in [
                "Makefile",
                "preamble.tex",
                "my.bib",
            ]:
                shutil.copy2(
                    ROOT / name, root / name
                )
            migrations = (
                "scripts/"
                "gerby_label_migrations.json"
            )
            shutil.copy2(
                ROOT / migrations,
                root / migrations,
            )
            (root / "registry").mkdir()
            baseline = (
                "0000,part-examples\n"
                "0001,chapter-sample\n"
                "0002,sample-section-first\n"
                "0003,sample-lemma-first\n"
                "#0004,sample-deleted\n"
            )
            for name in [
                "tags",
                "baseline.tags",
            ]:
                (
                    root / "registry" / name
                ).write_text(baseline)
            snapshot = {
                "path": (
                    "registry/baseline.tags"
                ),
                "sha256": hashlib.sha256(
                    baseline.encode()
                ).hexdigest(),
            }
            (
                root
                / "registry/history.json"
            ).write_text(
                json.dumps(
                    {
                        "version": 1,
                        "snapshots": [
                            snapshot
                        ],
                    }
                )
            )
            (
                root / "order-chapters.txt"
            ).write_text(
                "PART I: Examples\nSample\n"
            )
            self.source("first")
            self.make("gerby-import")
            self.startup()
            self.assertEqual(
                self.identities()["0003"],
                ("sample-lemma-first", 1),
            )
            database = (
                root / "gerby/stack.sqlite"
            )
            before = database.read_bytes()
            self.source("new")
            self.make(
                "gerby-import", success=False
            )
            self.assertEqual(
                before, database.read_bytes()
            )
            self.make("gerby-register")
            self.make("gerby-import")
            self.startup()
            self.assertEqual(
                self.identities()["0003"][1],
                0,
            )
            self.assertEqual(
                self.identities()["0005"],
                ("sample-lemma-new", 1),
            )
            self.source("first")
            self.make("gerby-import")
            self.startup()
            self.assertEqual(
                self.identities()["0003"],
                ("sample-lemma-first", 1),
            )

    def source(self, label):
        (
            self.root / "sample.tex"
        ).write_text(
            "\\title{Sample}\n"
            "\\begin{document}\n"
            "\\section{First}\n"
            "\\label{section-first}\n"
            "\\begin{lemma}\n"
            "\\label{lemma-" + label + "}\n"
            "A sample statement.\n"
            "\\end{lemma}\n"
            "\\end{document}\n"
        )

    def make(self, target, success=True):
        env = dict(os.environ)
        env["PATH"] = (
            str(Path(sys.executable).parent)
            + os.pathsep
            + env.get("PATH", "")
        )
        result = subprocess.run(
            [
                "make",
                target,
                "PYTHON=" + sys.executable,
                "GERBY_FILES=sample.tex",
            ],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
            timeout=90,
        )
        message = (
            result.stdout + result.stderr
        )
        self.assertEqual(
            result.returncode == 0,
            success,
            message[-5000:],
        )

    def identities(self):
        path = (
            self.root / "gerby/stack.sqlite"
        )
        with sqlite3.connect(path) as db:
            rows = db.execute(
                "SELECT tag,label,active "
                "FROM tag"
            )
            return {
                t: (label, active)
                for t, label, active in rows
            }

    def startup(self):
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import wsgi",
            ],
            cwd=self.root / "gerby-website",
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(
            result.returncode,
            0,
            result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
