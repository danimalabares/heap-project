import json
import os.path

from flask import redirect, render_template

from gerby.application import app
from gerby.configuration import DOWNLOADS, ROOT


def load_slides():
  """Read slides/index.json and mark which PDFs have been built."""
  path = os.path.join(str(ROOT), "slides", "index.json")
  if not os.path.isfile(path):
    return []

  with open(path) as f:
    index = json.load(f)

  for entry in index:
    for deck in entry.get("decks", [entry]):
      name = deck["path"].split("/")[-1]
      filename = os.path.join("slides", deck["path"] + ".pdf")
      deck["pdf"] = filename if os.path.isfile(os.path.join(DOWNLOADS, filename)) else None
      deck["source"] = "https://github.com/danimalabares/heap-project/blob/main/slides/%s/%s.tex" % (deck["path"], name)

  return index


@app.route("/talks")
def show_slides():
  return render_template("single/slides.html", slides=load_slides())


@app.route("/slides")
def redirect_slides():
  """The page was called /slides."""
  return redirect("/talks", code=301)


@app.route("/guitar")
def show_guitar():
  """Guitar practice: metronome with timed scale exercises, and the scales PDF.

  Static files, built from ~/music/guitar-practice by its make-public.py."""
  return redirect("/static/guitar/index.html")
