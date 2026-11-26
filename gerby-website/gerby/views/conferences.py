from flask import render_template

from gerby.application import CONFERENCES_PART_LABEL, app
from gerby.views.seminars import load_part_by_subject

# Subjects in display order, newest first (by the date of their
# latest conference), with the notebook (chapter file name without
# .tex) of each, newest first too.
SUBJECTS = [
  ("Analysis and PDE", ["waves-in-fluids-iv"]),
  ("Algebraic geometry", [
    "legal-2027",
    "vbac",
    "iv-jornadas-lefschetz-2026",
    "16th-alga-meeting-2026",
    "hodge-birational-atoms-2026",
  ]),
  ("Several areas of mathematics", ["oktobermat-2026", "oktobermat-2024"]),
  ("Economics", ["saet-2026"]),
  ("Differential geometry", [
    "xxii-egd-2026",
    "cimpa-el-salvador-2024",
  ]),
]


def load_conferences():
  """List the notebooks of the Conferences part by subject."""
  subjects = load_part_by_subject(CONFERENCES_PART_LABEL, SUBJECTS)
  return subjects


@app.route("/conferences")
def show_conferences():
  return render_template("single/conferences.html", subjects=load_conferences())
