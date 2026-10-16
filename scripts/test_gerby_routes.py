"""Exercise missing-tag HTTP behavior."""

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
import gerby.views.tag as view


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
        response = self.client.get(
            "/tag/ZZZZ"
        )
        self.assertEqual(
            response.status_code, 404
        )


if __name__ == "__main__":
    unittest.main()
