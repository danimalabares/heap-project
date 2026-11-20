from types import SimpleNamespace

from flask import render_template

from gerby.application import CONFERENCES_PART_LABEL, app
from gerby.views.seminars import load_part_by_subject

# Subjects in display order (by date of their first conference), with the notebook
# (chapter file name without .tex) of each.
SUBJECTS = [
  ("Differential geometry", [
    "cimpa-el-salvador-2024",
    "xxii-egd-2026",
  ]),
  ("Several areas of mathematics", ["oktobermat-2024", "oktobermat-2026"]),
  ("Algebraic geometry", [
    "hodge-birational-atoms-2026",
    "16th-alga-meeting-2026",
    "iv-jornadas-lefschetz-2026",
    "vbac",
    "legal-2027",
  ]),
  ("Economics", ["saet-2026"]),
  ("Analysis and PDE", ["waves-in-fluids-iv"]),
]


# Notes of conferences kept only as the original PDF (not
# HP notebooks), listed in date order with the notebooks.
OAXACA_2023 = SimpleNamespace(
  tag=None,
  name="CIMPA Research School Oaxaca 2023: "
       "Algebraic and Tropical Methods for Solving "
       "Differential Equations",
  pdf=None,
  href="/standalone/cimpa-oaxaca-2023.pdf",
  source="https://github.com/danimalabares/heap-project/"
         "tree/main/standalone/sources/cimpa-oaxaca-2023",
)


def load_conferences():
  """List the notebooks of the Conferences part by subject."""
  subjects = load_part_by_subject(CONFERENCES_PART_LABEL, SUBJECTS)
  # Oaxaca 2023 is the earliest conference, so its subject goes first.
  group = next((s for s in subjects if s[0] == "Analysis and PDE"), None)
  if group is None:
    group = ("Analysis and PDE", [])
  else:
    subjects.remove(group)
  group[1].insert(0, OAXACA_2023)
  subjects.insert(0, group)
  return subjects


@app.route("/conferences")
def show_conferences():
  return render_template("single/conferences.html", subjects=load_conferences())
