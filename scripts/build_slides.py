#!/usr/bin/env python3
"""Build the beamer decks listed in slides/index.json.

The manifest is a list. An entry is either a deck, with a "path"
<series>/<deck>, or a group with a "title" and a list "decks".
Each deck slides/<series>/<deck>/<deck>.tex is compiled twice
with pdflatex in a temporary directory, and the PDF is copied to
gerby/downloads/slides/<series>/<deck>.pdf, where the website
serves it as /download/slides/<series>/<deck>.pdf.

A deck that fails to build is reported and skipped; the exit
status is 1 if any deck failed.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / "slides"
OUT = ROOT / "gerby" / "downloads" / "slides"


def build(series, deck):
    source_dir = SLIDES / series / deck
    source = source_dir / (deck + ".tex")
    if not source.is_file():
        print("missing source: %s" % source)
        return False
    with tempfile.TemporaryDirectory() as tmp:
        command = [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-output-directory=" + tmp,
            source.name,
        ]
        for _ in range(2):
            result = subprocess.run(
                command,
                cwd=str(source_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if result.returncode != 0:
                tail = result.stdout.decode("utf-8", "replace")
                print("\n".join(tail.splitlines()[-25:]))
                print("FAILED: %s/%s" % (series, deck))
                return False
        target = OUT / series / (deck + ".pdf")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(Path(tmp) / (deck + ".pdf")), str(target))
        print("built %s" % target.relative_to(ROOT))
    return True


def main():
    with open(str(SLIDES / "index.json")) as handle:
        index = json.load(handle)
    ok = True
    for entry in index:
        for deck in entry.get("decks", [entry]):
            series, name = deck["path"].split("/")
            ok = build(series, name) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
