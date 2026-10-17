"""Render fancyvrb options through plasTeX."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name(
    "plastex_gerby.py"
)


class FancyvrbTests(unittest.TestCase):
    def test_macro_fontsize(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "book.tex").write_text(
                "\\documentclass{book}\n"
                "\\usepackage{fancyvrb}\n"
                "\\begin{document}\n"
                "\\chapter{A}\\label{chapter-a}\n"
                "\\begin{Verbatim}"
                "[fontsize=\\footnotesize]\n"
                "first text\n"
                "\\end{Verbatim}\n"
                "\\begin{Verbatim}"
                "[frame=single,fontsize=\\small]\n"
                "second text\n"
                "\\end{Verbatim}\n"
                "\\end{document}\n"
            )
            (root / "tags").write_text(
                "0000,chapter-a\n"
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
            html = "".join(
                path.read_text()
                for path in (root / "out").glob(
                    "*.tag"
                )
            )
            self.assertIn("first text", html)
            self.assertIn("second text", html)


if __name__ == "__main__":
    unittest.main()
