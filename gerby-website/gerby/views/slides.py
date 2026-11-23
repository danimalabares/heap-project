import json
import os.path

from flask import abort, redirect, render_template, send_from_directory

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


@app.route("/talks/<series>/<deck>/<name>.html")
def show_model(series, deck, name):
  """An interactive page of a talk: a file listed under "models" in
  slides/index.json, served from the talk's own folder."""
  path = "%s/%s" % (series, deck)
  for entry in load_slides():
    for item in entry.get("decks", [entry]):
      if item["path"] == path:
        if name + ".html" in [m["file"] for m in item.get("models", [])]:
          folder = os.path.join(str(ROOT), "slides", series, deck)
          return send_from_directory(folder, name + ".html")
  abort(404)


@app.route("/slides")
def redirect_slides():
  """The page was called /slides."""
  return redirect("/talks", code=301)


@app.route("/guitar")
def show_guitar():
  """Guitar practice: metronome with timed scale exercises, and the scales PDF.

  Static files, built from ~/music/guitar-practice by its make-public.py."""
  return redirect("/static/guitar/index.html")
