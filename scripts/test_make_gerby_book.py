import tempfile
import unittest
from pathlib import Path

from make_gerby_book import body_for


class MathPreservationTests(unittest.TestCase):
    def test_math_commands_survive_conversion(self):
        formulas = [
            r"W:Y\longrightarrow\mathbb{C}.",
            r"q\in\mathbb{C}^{*}",
            r"V\cong\mathbb{R}^n",
            r"x\in\text{domain}",
            r"\text{a {nested} label}",
        ]
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "chapter.tex"
            source.write_text(
                "\\begin{document}\n"
                "\\section{Formulas}\n$$\n"
                + "\n".join(formulas)
                + "\n$$\n\\end{document}\n",
                encoding="utf-8",
            )
            rendered = body_for(source)
        for formula in formulas:
            with self.subTest(formula=formula):
                self.assertIn(formula, rendered)


class LabelIdentityTests(unittest.TestCase):
    def test_duplicate_labels_fail(self):
        from make_gerby_book import (
            prefix_labels_and_refs,
        )

        counts = {}
        prefix_labels_and_refs(
            r'\label{same}', 'chapter', counts
        )
        with self.assertRaises(ValueError):
            prefix_labels_and_refs(
                r'\label{same}', 'chapter', counts
            )


if __name__ == "__main__":
    unittest.main()
