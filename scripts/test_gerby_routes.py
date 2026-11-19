"""Exercise missing-tag HTTP behavior."""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(
    0, str(ROOT / "gerby-website")
)

from gerby.application import app
from gerby.database import (
    History,
    Part,
    Reference,
    Slogan,
    Tag,
    db,
)
import gerby.registry as registry
import gerby.views.seminars as seminars_view
import gerby.views.tag as view
import gerby.application as application
from gerby_registry import Evidence


class MissingTagTests(unittest.TestCase):
    def setUp(self):
        self.tmp = (
            tempfile.TemporaryDirectory()
        )
        self.addCleanup(self.tmp.cleanup)
        self.tags = (
            Path(self.tmp.name) / "tags"
        )
        self.tags.write_text(
            "#0000,chapter-old\n"
            "0001,chapter-paragraph\n"
            "0002,chapter-new\n"
        )
        root = Path(self.tmp.name)
        snapshots = []
        for name, role, text in [
            (
                "base.tags",
                "canonical",
                self.tags.read_text(),
            ),
            (
                "old.tags",
                "legacy",
                "0002,chapter-older\n"
                "0003,chapter-gone\n"
                "0004,chapter-a\n",
            ),
            (
                "older.tags",
                "legacy",
                "0004,chapter-b\n",
            ),
        ]:
            (root / name).write_text(text)
            snapshots.append(
                {
                    "path": name,
                    "role": role,
                    "sha256": hashlib.sha256(
                        text.encode()
                    ).hexdigest(),
                }
            )
        history = root / "history.json"
        history.write_text(
            json.dumps(
                {
                    "version": 2,
                    "allocation_floor": "0100",
                    "snapshots": snapshots,
                }
            )
        )
        patcher = patch.object(
            registry,
            "evidence",
            return_value=Evidence(
                history, root, {}
            ),
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        db.init(":memory:")
        db.connect()
        db.create_tables(
            [
                Tag,
                Slogan,
                History,
                Reference,
            ]
        )
        self.addCleanup(db.close)
        Tag.create(
            tag="0000",
            label="chapter-old",
            active=False,
            ref="1",
            type="chapter",
        )
        Tag.create(
            tag="0002",
            label="chapter-new",
            active=True,
            ref="1",
            type="chapter",
        )
        patcher = patch.object(
            view.gerby.configuration,
            "TAGS",
            str(self.tags),
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch.object(
            view,
            "render_template",
            return_value="Unavailable",
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.client = app.test_client()

    def test_retired_no_number_redirect(
        self,
    ):
        response = self.client.get(
            "/tag/0000"
        )
        self.assertEqual(
            response.status_code, 410
        )
        self.assertNotIn(
            "Location", response.headers
        )

    def test_tombstone_without_database_row(
        self,
    ):
        Tag.delete().where(
            Tag.tag == "0000"
        ).execute()
        response = self.client.get(
            "/tag/0000"
        )
        self.assertEqual(
            response.status_code, 410
        )

    def test_missing_does_not_guess_chapter(
        self,
    ):
        response = self.client.get(
            "/tag/0001"
        )
        self.assertEqual(
            response.status_code, 404
        )
        self.assertNotIn(
            "Location", response.headers
        )

    def test_unknown_returns_404(self):
        for tag in ["ZZZZ", "0050"]:
            response = self.client.get(
                "/tag/" + tag
            )
            self.assertEqual(
                response.status_code, 404
            )

    def test_historical_tags_are_gone(
        self,
    ):
        # One or several old meanings:
        # never a redirect or a guess.
        for tag in ["0003", "0004"]:
            response = self.client.get(
                "/tag/" + tag
            )
            self.assertEqual(
                response.status_code, 410
            )
            self.assertNotIn(
                "Location", response.headers
            )

    def test_provenance_page(self):
        for tag, status in [
            ("0002", "active"),
            ("0000", "retired"),
            ("0003", "historical"),
            ("0004", "ambiguous"),
            ("0050", "reserved"),
            ("ZZZZ", "unknown"),
        ]:
            with patch.object(
                view,
                "render_template",
                return_value="page",
            ) as render:
                response = self.client.get(
                    "/tag/" + tag + "/provenance"
                )
            self.assertEqual(
                response.status_code, 200
            )
            info = render.call_args.kwargs[
                "info"
            ]
            self.assertEqual(
                info["status"], status
            )
        self.assertTrue(
            registry.describe(
                "0002", str(self.tags)
            )["conflicting"]
        )
        response = self.client.get(
            "/tag/O0O0/provenance"
        )
        self.assertEqual(
            response.status_code, 404
        )


class ContentsAndDownloadsTests(
    unittest.TestCase
):
    def test_parts_use_numeric_order(self):
        db.init(":memory:")
        db.connect()
        self.addCleanup(db.close)
        db.create_tables([Tag, Part])
        for number in [10, 2, 1]:
            part = Tag.create(
                tag="P%03d" % number,
                label="part-%d" % number,
                ref=str(number),
                type="part",
                active=True,
            )
            chapter = Tag.create(
                tag="C%03d" % number,
                label="chapter-%d" % number,
                ref=str(number),
                type="chapter",
                active=True,
            )
            Part.create(
                part=part, chapter=chapter
            )
        with patch.object(
            application, "render_template",
            return_value="Contents",
        ) as render:
            response = app.test_client().get(
                "/browse"
            )
        self.assertEqual(
            response.status_code, 200
        )
        parts = render.call_args.kwargs[
            "parts"
        ]
        self.assertEqual(
            [p.ref for p in parts],
            ["1", "2", "10"],
        )

    def make_parts(self):
        db.init(":memory:")
        db.connect()
        self.addCleanup(db.close)
        db.create_tables([Tag, Part])
        theory = Tag.create(
            tag="P001", label="part-analysis",
            ref="1", type="part", active=True,
        )
        seminars = Tag.create(
            tag="P002", label="part-seminars",
            ref="2", type="part", active=True,
        )
        for part, tag, name in [
            (theory, "C001", "pde"),
            (seminars, "C002", "seminars-others"),
            (
                seminars, "C003",
                "seminars-analysis-pde",
            ),
            (seminars, "C004", "seminars-new"),
        ]:
            chapter = Tag.create(
                tag=tag, label="chapter-" + name,
                ref=tag[-1], type="chapter",
                active=True, name=name,
            )
            Part.create(
                part=part, chapter=chapter
            )

    def test_browse_hides_seminars(self):
        self.make_parts()
        with patch.object(
            application, "render_template",
            return_value="Contents",
        ) as render:
            response = app.test_client().get(
                "/browse"
            )
        self.assertEqual(
            response.status_code, 200
        )
        parts = render.call_args.kwargs[
            "parts"
        ]
        self.assertEqual(
            [p.label for p in parts],
            ["part-analysis"],
        )

    def test_seminars_page_lists_by_subject(
        self,
    ):
        self.make_parts()
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        (
            Path(tmp.name)
            / "seminars-others.pdf"
        ).write_bytes(b"%PDF-1.4 test")
        patcher = patch.object(
            seminars_view, "DOWNLOADS",
            tmp.name,
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        with patch.object(
            seminars_view, "render_template",
            return_value="Seminars",
        ) as render:
            response = app.test_client().get(
                "/seminars"
            )
        self.assertEqual(
            response.status_code, 200
        )
        subjects = render.call_args.kwargs[
            "subjects"
        ]
        self.assertEqual(
            [
                (
                    subject,
                    [c.tag for c in chapters],
                )
                for subject, chapters
                in subjects
            ],
            [
                ("Analysis and PDE", ["C003"]),
                (
                    "Other subjects",
                    ["C002", "C004"],
                ),
            ],
        )
        others = subjects[1][1][0]
        self.assertEqual(
            others.pdf, "seminars-others.pdf"
        )
        self.assertIsNone(subjects[1][1][1].pdf)

    def test_published_pdf_downloads(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        names = [
            "history", "anthropology",
            "historia-do-brasil",
            "genealogia-familiar", "religion",
        ]
        for name in names:
            path = Path(tmp.name) / (
                name + ".pdf"
            )
            path.write_bytes(b"%PDF-1.4 test")
        patcher = patch.object(
            application, "DOWNLOADS", tmp.name
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        client = app.test_client()
        for name in names:
            with self.subTest(name=name):
                response = client.get(
                    "/download/" + name
                    + ".pdf"
                )
                self.assertEqual(
                    response.status_code, 200
                )
                self.assertEqual(
                    response.data,
                    b"%PDF-1.4 test",
                )
                response.close()
        response = client.get(
            "/download/missing.pdf"
        )
        self.assertEqual(
            response.status_code, 404
        )


if __name__ == "__main__":
    unittest.main()
