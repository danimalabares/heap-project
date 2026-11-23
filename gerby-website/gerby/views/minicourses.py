from flask import render_template

from gerby.application import MINICOURSES_PART_LABEL, app
from gerby.views.seminars import load_part_by_subject

# Events in display order, newest first, with
# the notebook (chapter file name without .tex)
# of each minicourse.
EVENTS = [
  ("OPEGA 2026, UFPE", [
    "birational-maps-commutative-algebra",
    "cremona-transformations",
  ]),
  ("IMPA Summer School 2026", [
    "mumford-tate-groups-in-hodge-theory",
    "surfaces",
  ]),
  ("CIMPA school Florianópolis 2025", [
    "noncommutative-abelian-surfaces-and-kummer-type-hyperkahler-varieties",
    "derived-categories-of-sheaves",
    "geometric-invariant-theory",
    "moduli-spaces-of-sheaves",
    "geometric-stability-conditions-and-group-actions",
    "bridgeland-stability-general-theory",
  ]),
  ("Summer 2024", [
    "quantum-groups",
  ]),
]

LECTURERS = {
  "quantum-groups": "Artem Kalmykov",
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
      chapter.lecturer = LECTURERS.get(chapter.notebook)
  return events


@app.route("/minicourses")
def show_minicourses():
  return render_template("single/minicourses.html", subjects=load_minicourses())
