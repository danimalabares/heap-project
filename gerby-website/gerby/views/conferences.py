from flask import render_template

from gerby.application import CONFERENCES_PART_LABEL, app
from gerby.views.seminars import load_part_by_subject

# Subjects in display order, with the notebook
# (chapter file name without .tex) of each.
SUBJECTS = [
  ("Differential geometry", [
    "cimpa-el-salvador-2024",
    "xxii-egd-2026",
  ]),
  ("Analysis and PDE", ["waves-in-fluids-iv"]),
  ("Algebraic geometry", [
    "hodge-birational-atoms-2026",
    "16th-alga-meeting-2026",
    "iv-jornadas-lefschetz-2026",
    "vbac",
  ]),
]


def load_conferences():
  """List the notebooks of the Conferences part by subject."""
  return load_part_by_subject(CONFERENCES_PART_LABEL, SUBJECTS)


@app.route("/conferences")
def show_conferences():
  return render_template("single/conferences.html", subjects=load_conferences())
