import json
import os.path

from flask import render_template

from gerby.application import app
from gerby.configuration import DOWNLOADS, ROOT


def load_slides():
  """Read slides/index.json and mark which PDFs have been built."""
  path = os.path.join(str(ROOT), "slides", "index.json")
  if not os.path.isfile(path):
    return []

  with open(path) as f:
    index = json.load(f)

  for series in index:
    for deck in series["decks"]:
      filename = os.path.join("slides", series["series"], deck["deck"] + ".pdf")
      deck["pdf"] = filename if os.path.isfile(os.path.join(DOWNLOADS, filename)) else None
      deck["source"] = "https://github.com/danimalabares/heap-project/blob/main/slides/%s/%s/%s.tex" % (series["series"], deck["deck"], deck["deck"])

  return index


@app.route("/slides")
def show_slides():
  return render_template("single/slides.html", slides=load_slides())
