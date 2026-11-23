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
import gerby.views.conferences as conferences_view
import gerby.views.minicourses as minicourses_view
import gerby.views.seminars as seminars_view
import gerby.views.tag as view
import gerby.talks as talks
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
        conferences = Tag.create(
            tag="P003", label="part-conferences",
            ref="3", type="part", active=True,
        )
        minicourses = Tag.create(
            tag="P004", label="part-minicourses",
            ref="4", type="part", active=True,
        )
        for part, tag, name in [
            (minicourses, "C007", "surfaces"),
            (
                minicourses, "C008",
                "geometric-stability-conditions"
                "-and-group-actions"
                "-section-motivation",
            ),
            (conferences, "C005", "vbac"),
            (
                conferences, "C006",
                "xxii-egd-2026",
            ),
            (theory, "C001", "pde"),
            (seminars, "C002", "seminars-algebra"),
            (
                seminars, "C003",
                "seminars-analysis-pde",
            ),
            (seminars, "C004", "seminars-new"),
        ]:
            chapter = Tag.create(
                tag=tag,
                label=(
                    name
                    if "-section-" in name
                    else "chapter-" + name
                ),
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
            / "seminars-algebra.pdf"
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
                ("Algebra", ["C002"]),
                ("Computing", ["C004"]),
            ],
        )
        self.assertEqual(
            subjects[1][1][0].pdf,
            "seminars-algebra.pdf",
        )
        self.assertIsNone(subjects[2][1][0].pdf)

    def test_conferences_page_lists_by_subject(
        self,
    ):
        self.make_parts()
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        (
            Path(tmp.name) / "vbac.pdf"
        ).write_bytes(b"%PDF-1.4 test")
        patcher = patch.object(
            seminars_view, "DOWNLOADS",
            tmp.name,
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        with patch.object(
            conferences_view, "render_template",
            return_value="Conferences",
        ) as render:
            response = app.test_client().get(
                "/conferences"
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
                ("Analysis and PDE", [None]),
                (
                    "Differential geometry",
                    ["C006"],
                ),
                ("Algebraic geometry", ["C005"]),
            ],
        )
        self.assertEqual(
            subjects[2][1][0].pdf, "vbac.pdf"
        )

    def test_minicourses_page_lists_by_event(
        self,
    ):
        self.make_parts()
        with patch.object(
            minicourses_view, "render_template",
            return_value="Minicourses",
        ) as render:
            response = app.test_client().get(
                "/minicourses"
            )
        self.assertEqual(
            response.status_code, 200
        )
        events = render.call_args.kwargs[
            "subjects"
        ]
        self.assertEqual(
            [
                (event, [c.tag for c in chapters])
                for event, chapters in events
            ],
            [
                (
                    "CIMPA school Florianópolis 2025",
                    ["C008"],
                ),
                (
                    "IMPA Summer School 2026",
                    ["C007"],
                ),
            ],
        )
        self.assertEqual(
            events[0][1][0].lecturer,
            "Hannah Dell",
        )
        self.assertEqual(
            events[1][1][0].lecturer,
            "Aline Zanardini",
        )

    def test_talk_metadata_of_a_section(self):
        text = (
            "\\section{T}\n"
            "\\label{%\nsection-a%\n}\n"
            "%% speaker: Ann Lee, Univ\n"
            "%% speaker: of Somewhere\n"
            "%% place: Seminar, IMPA\n"
            "%% date: May 1, 2026\n\n"
            "\\section{U}\n\\label{section-b}\n"
            "Text.\n"
        )
        found = talks.parse_file("nb", text)
        self.assertEqual(
            found,
            {
                "nb-section-a": (
                    "Ann Lee, Univ of Somewhere",
                    "Seminar, IMPA",
                    "May 1, 2026",
                )
            },
        )
        self.assertEqual(
            talks.describe(found["nb-section-a"]),
            "Ann Lee, Univ of Somewhere."
            " Seminar, IMPA. May 1, 2026.",
        )

    def test_seminar_notebooks_record_talks(self):
        for name in [
            "seminars-analysis-pde",
            "seminars-differential-geometry",
            "seminars-symplectic-geometry",
            "seminars-complex-geometry",
            "seminars-algebraic-geometry",
            "seminars-algebra",
            "seminars-physics",
            "seminars-computing",
            "seminars-dynamics",
            "oktobermat-2024",
            "oktobermat-2026",
            "saet-2026",
        ]:
            text = (ROOT / (name + ".tex")).read_text(
                encoding="utf-8"
            )
            sections = text.count("\\section{")
            recorded = len(
                talks.parse_file(name, text)
            )
            self.assertEqual(
                sections, recorded, name
            )

    def test_talks_page_and_old_slides_url(self):
        client = app.test_client()
        page = client.get("/talks")
        self.assertEqual(page.status_code, 200)
        old = client.get("/slides")
        self.assertEqual(old.status_code, 301)
        self.assertTrue(
            old.headers["Location"].endswith("/talks")
        )

    def test_talks_are_in_chronological_order(self):
        from gerby.views.slides import date_key, load_slides

        self.assertLess(
            date_key({"date": "November 2026"}),
            date_key({"date": "16 November 2026"}),
        )
        self.assertLess(
            date_key({"date": "3 December 2026"}),
            date_key({"date": "In preparation"}),
        )
        index = load_slides()
        firsts = [date_key(e.get("decks", [e])[0]) for e in index]
        self.assertEqual(firsts, sorted(firsts))
        for entry in index:
            keys = [date_key(d) for d in entry.get("decks", [])]
            self.assertEqual(keys, sorted(keys))

        client = app.test_client()
        base = "/talks/stanley-reisner-puc-informal/"
        page = client.get("/talks").get_data(as_text=True)
        self.assertIn(base + "from-a-vertex.html", page)
        for name in ("from-a-vertex.html", "from-a-vertex-4d.html"):
            got = client.get(base + name)
            self.assertEqual(got.status_code, 200, name)
            self.assertIn("text/html", got.content_type)
        # Only files listed in slides/index.json are served.
        for name in ("preamble.html", "nothing.html"):
            self.assertEqual(client.get(base + name).status_code, 404)
        # Former addresses: with the series, and the old file names.
        old = client.get("/talks/talks/stanley-reisner-puc-informal/spheres-2d.html")
        self.assertEqual(old.status_code, 301)
        self.assertTrue(old.headers["Location"].endswith(base + "spheres-2d.html"))
        old = client.get(base + "spheres-2d.html")
        self.assertEqual(old.status_code, 301)
        self.assertTrue(old.headers["Location"].endswith(base + "from-a-vertex.html"))
        # The address has no series, so deck names must not repeat.
        index = json.loads((ROOT / "slides" / "index.json").read_text())
        names = [
            deck["path"].split("/")[-1]
            for entry in index
            for deck in entry.get("decks", [entry])
        ]
        self.assertEqual(len(names), len(set(names)))

    def test_standalone_page_and_old_urls(self):
        client = app.test_client()
        page = client.get("/standalone")
        self.assertEqual(page.status_code, 200)
        text = page.get_data(as_text=True)
        self.assertIn("Course notes", text)
        self.assertIn("End-of-course project", text)
        self.assertIn("Master’s tesina", text)
        self.assertNotIn("<h3", text)
        self.assertNotIn("cimpa-oaxaca", text)
        pdf = client.get(
            "/standalone/combinatoria.pdf"
        )
        self.assertEqual(pdf.status_code, 200)
        pdf.close()
        for old, new in [
            ("/course-projects", "/standalone"),
            (
                "/course-projects/combinatoria.pdf",
                "/standalone/combinatoria.pdf",
            ),
        ]:
            response = client.get(old)
            self.assertEqual(
                response.status_code, 301
            )
            self.assertTrue(
                response.headers["Location"]
                .endswith(new)
            )

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
