import os.path

from flask import abort, send_from_directory

from gerby.application import app
from gerby.configuration import ROOT


@app.route("/models/<chapter>/<name>.html")
def show_chapter_model(chapter, name):
  """An interactive page of a chapter: a self-contained HTML file kept in
  the chapter's own folder <chapter>-assets, next to its figures."""
  folder = os.path.join(str(ROOT), chapter + "-assets")
  if not os.path.isfile(os.path.join(folder, name + ".html")):
    abort(404)
  return send_from_directory(folder, name + ".html")
