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
    Reference,
    Slogan,
    Tag,
    db,
)
import gerby.registry as registry
import gerby.views.tag as view
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


if __name__ == "__main__":
    unittest.main()
