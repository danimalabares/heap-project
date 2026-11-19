import os.path

from flask import render_template

from gerby.application import SEMINARS_PART_LABEL, app
from gerby.configuration import DOWNLOADS
from gerby.database import Part, Tag

# Subjects in display order, with the notebook
# (chapter file name without .tex) of each.
SUBJECTS = [
  ("Analysis and PDE", ["seminars-analysis-pde"]),
  ("Differential geometry", ["seminars-differential-geometry"]),
  ("Complex geometry", ["seminars-complex-geometry"]),
  ("Algebraic geometry", ["seminars-algebraic-geometry"]),
  ("Other subjects", ["seminars-others"]),
]


def load_seminars():
  """List the notebooks of the Seminars part by subject."""
  part = Tag.select().where(Tag.label == SEMINARS_PART_LABEL).first()
  if part is None:
    return []

  notebooks = {}
  for row in Part.select().where(Part.part == part.tag):
    chapter = row.chapter
    name = chapter.label[len("chapter-"):]
    filename = name + ".pdf"
    chapter.pdf = filename if os.path.isfile(os.path.join(DOWNLOADS, filename)) else None
    chapter.source = "https://github.com/danimalabares/heap-project/blob/main/%s.tex" % name
    notebooks[name] = chapter

  subjects = []
  for subject, names in SUBJECTS:
    found = [notebooks.pop(name) for name in names if name in notebooks]
    subjects.append((subject, found))

  # A notebook added to the part but not yet
  # assigned a subject is listed with the others.
  if notebooks:
    subjects[-1][1].extend(sorted(notebooks.values()))

  return [(subject, found) for subject, found in subjects if found]


@app.route("/seminars")
def show_seminars():
  return render_template("single/seminars.html", subjects=load_seminars())
