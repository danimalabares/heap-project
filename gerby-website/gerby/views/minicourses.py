from flask import render_template

from gerby.application import MINICOURSES_PART_LABEL, app
from gerby.views.seminars import load_part_by_subject

# Events in display order, with the notebook
# (chapter file name without .tex) of each
# minicourse.
EVENTS = [
  ("CIMPA school Florianópolis 2025", [
    "bridgeland-stability-general-theory",
    "geometric-stability-conditions-and-group-actions",
    "moduli-spaces-of-sheaves",
    "geometric-invariant-theory",
    "derived-categories-of-sheaves",
    "noncommutative-abelian-surfaces-and-kummer-type-hyperkahler-varieties",
  ]),
  ("OPEGA 2026, UFPE", [
    "cremona-transformations",
    "birational-maps-commutative-algebra",
  ]),
  ("IMPA Summer School 2026", [
    "surfaces",
    "mumford-tate-groups-in-hodge-theory",
  ]),
]

LECTURERS = {
  "bridgeland-stability-general-theory": "Cristian Martinez",
  "geometric-stability-conditions-and-group-actions": "Hannah Dell",
  "moduli-spaces-of-sheaves": "Cristina Manolache",
  "geometric-invariant-theory": "Michel Brion",
  "derived-categories-of-sheaves": "Lyalya Guseva",
  "noncommutative-abelian-surfaces-and-kummer-type-hyperkahler-varieties": "Xiaolei Zhao",
  "cremona-transformations": "Carolina Araujo and Sokratis Zikas",
  "birational-maps-commutative-algebra": "Hamid Hassanzadeh",
  "surfaces": "Aline Zanardini",
  "mumford-tate-groups-in-hodge-theory": "Andrey Soldatenkov",
}


def load_minicourses():
  """List the notebooks of the Minicourses part by event."""
  events = load_part_by_subject(MINICOURSES_PART_LABEL, EVENTS)
  for event, chapters in events:
    for chapter in chapters:
      name = chapter.label[len("chapter-"):]
      chapter.lecturer = LECTURERS.get(name)
  return events


@app.route("/minicourses")
def show_minicourses():
  return render_template("single/minicourses.html", subjects=load_minicourses())
