import json
import os.path

from flask import abort, redirect, render_template, send_from_directory

from gerby.application import app
from gerby.configuration import DOWNLOADS, ROOT
from gerby.talks import date_key


def load_slides():
  """Read slides/index.json, newest talk first, and mark which PDFs
  have been built. A group stands at the date of its latest talk.
  Talks with the same date keep the order of the file."""
  path = os.path.join(str(ROOT), "slides", "index.json")
  if not os.path.isfile(path):
    return []

  with open(path) as f:
    index = json.load(f)

  for entry in index:
    if "decks" in entry:
      entry["decks"].sort(key=lambda deck: date_key(deck.get("date", "")), reverse=True)
  index.sort(key=lambda entry: date_key(entry.get("decks", [entry])[0].get("date", "")), reverse=True)

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


@app.route("/talks/<deck>/<name>.html")
def show_model(deck, name):
  """An interactive page of a talk: a file listed under "models" in
  slides/index.json, served from the talk's own folder. A former
  name of the file (listed under "was") redirects to it."""
  name = name + ".html"
  for entry in load_slides():
    for item in entry.get("decks", [entry]):
      if item["path"].split("/")[-1] != deck:
        continue
      for model in item.get("models", []):
        if name == model["file"]:
          folder = os.path.join(str(ROOT), "slides", item["path"])
          return send_from_directory(folder, name)
        if name in model.get("was", []):
          return redirect("/talks/%s/%s" % (deck, model["file"]), code=301)
  abort(404)


@app.route("/talks/<series>/<deck>/<name>.html")
def redirect_model(series, deck, name):
  """The address used to contain the series."""
  return redirect("/talks/%s/%s.html" % (deck, name), code=301)


@app.route("/slides")
def redirect_slides():
  """The page was called /slides."""
  return redirect("/talks", code=301)


@app.route("/guitar")
def show_guitar():
  """Guitar practice: metronome with timed scale exercises, and the scales PDF.

  Static files, built from ~/music/guitar-practice by its make-public.py."""
  return redirect("/static/guitar/index.html")
