"""Keep theorem-like environments consistent."""

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).with_name(
    "plastex_gerby.py"
)
SITE = ROOT / "gerby-website" / "gerby"
TYPE_LISTS = [
    SITE / "tools" / "update.py",
    SITE / "views" / "stacks.py",
    SITE / "templates" / "macros.html",
    SITE / "templates" / "single" / "statistics.html",
    SITE / "static" / "js" / "environment-links.js",
]


def preamble_environments():
    text = (ROOT / "preamble.tex").read_text()
    return set(
        re.findall(
            r"^\\newtheorem\{([a-z]+)\}",
            text,
            re.M,
        )
    )


class EnvironmentTests(unittest.TestCase):
    def test_corollary_shares_numbering(self):
        text = (ROOT / "preamble.tex").read_text()
        self.assertIn(
            "\\newtheorem{corollary}"
            "[subsection]{Corollary}",
            text,
        )

    def test_website_knows_every_environment(self):
        names = preamble_environments()
        self.assertIn("corollary", names)
        for path in TYPE_LISTS:
            text = path.read_text()
            for name in names:
                self.assertIn(
                    '"%s"' % name,
                    text,
                    "%s misses %s" % (path.name, name),
                )

    def test_no_lemma_titled_corollary(self):
        pattern = re.compile(
            r"\\begin\{lemma\}\s*\[\s*corollary",
            re.I,
        )
        make = (ROOT / "Makefile").read_text()
        files = re.search(
            r"^GERBY_FILES \?= (.*)$", make, re.M
        ).group(1).split()
        for name in files:
            text = (ROOT / name).read_text()
            self.assertIsNone(
                pattern.search(text), name
            )

    def test_corollary_keeps_its_tag(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "book.tex").write_text(
                "\\documentclass{book}\n"
                "\\usepackage{amsthm}\n"
                "\\newtheorem{lemma}"
                "[subsection]{Lemma}\n"
                "\\newtheorem{corollary}"
                "[subsection]{Corollary}\n"
                "\\begin{document}\n"
                "\\chapter{A}\\label{chapter-a}\n"
                "\\section{B}\\label{section-b}\n"
                "\\begin{lemma}\n"
                "\\label{lemma-first}\n"
                "First text.\n"
                "\\end{lemma}\n"
                "\\begin{corollary}[Named]\n"
                "\\label{lemma-second}\n"
                "Second text.\n"
                "\\end{corollary}\n"
                "\\end{document}\n"
            )
            (root / "tags").write_text(
                "0000,chapter-a\n"
                "0001,section-b\n"
                "0002,lemma-first\n"
                "0003,lemma-second\n"
            )
            env = dict(os.environ)
            env["PATH"] = (
                str(Path(sys.executable).parent)
                + os.pathsep
                + env.get("PATH", "")
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--renderer=Gerby",
                    "--tags=tags",
                    "--dir=out",
                    "book.tex",
                ],
                cwd=root,
                env=env,
                input="y\n",
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertEqual(
                result.returncode,
                0,
                result.stderr[-3000:],
            )
            names = sorted(
                path.name
                for path in (root / "out").glob(
                    "*.tag"
                )
            )
            second = [n for n in names if "0003" in n]
            self.assertEqual(len(second), 1, names)
            self.assertTrue(
                second[0].startswith("corollary-"),
                second[0],
            )
            self.assertTrue(
                second[0].endswith("lemma-second.tag"),
                second[0],
            )
            html = (root / "out" / second[0]).read_text()
            self.assertIn("Corollary", html)
            self.assertIn("Named", html)
            first = [n for n in names if "0002" in n]
            self.assertTrue(
                first[0].startswith("lemma-"),
                first[0],
            )


if __name__ == "__main__":
    unittest.main()
