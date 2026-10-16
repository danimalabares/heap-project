"""Regression tests for stable Gerby tag identities."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("gerby_tagger.py")


class TagStabilityTests(unittest.TestCase):
    def test_removed_label_recovers_its_original_tag(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tex = root / "book.tex"
            tags = root / "tags"

            def run(labels):
                tex.write_text("".join(
                    "\\label{" + label + "}\n" for label in labels
                ), encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), str(tex),
                     "--tags", str(tags)],
                    capture_output=True, text=True, check=True,
                )
                tags.write_text(result.stdout, encoding="utf-8")
                return result.stdout.splitlines()

            first = run(["alpha", "beta"])
            alpha = next(line.split(",")[0] for line in first
                         if line.endswith(",alpha"))
            beta = next(line.split(",")[0] for line in first
                        if line.endswith(",beta"))

            second = run(["beta"])
            self.assertIn("#" + alpha + ",alpha", second)

            third = run(["beta", "gamma"])
            gamma = next(line.split(",")[0] for line in third
                         if line.endswith(",gamma"))
            self.assertNotIn(gamma, [alpha, beta])
            self.assertIn("#" + alpha + ",alpha", third)

            fourth = run(["alpha", "beta", "gamma"])
            self.assertIn(alpha + ",alpha", fourth)
            self.assertNotIn("#" + alpha + ",alpha", fourth)

    def test_highest_reserved_tag_never_reused(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tex = root / "book.tex"
            tags = root / "tags"
            tags.write_text("#000Z,removed\n", encoding="utf-8")
            tex.write_text("\\label{new}\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(tex),
                 "--tags", str(tags)],
                capture_output=True, text=True, check=True,
            )
            self.assertIn("#000Z,removed", result.stdout)
            self.assertNotIn("000Z,new", result.stdout)


if __name__ == "__main__":
    unittest.main()
