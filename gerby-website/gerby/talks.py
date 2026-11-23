"""Speaker, place and date of the talks of the seminar notebooks.

A section of a seminar notebook records its talk in comment
lines right after its \\label:

  %% speaker: Name, Affiliation
  %% place: Seminar, Institution
  %% date: September 12, 2024

A value may continue on further lines with the same key.
The table of contents of the website shows them under
the title of the section.
"""
import re
from functools import lru_cache

from gerby.configuration import ROOT

KEYS = ("speaker", "place", "date")

SECTION = re.compile(
  r"\\label\{([^{}]*)\}[ \t]*\n((?:%% [a-z]+:[^\n]*\n)+)"
)


def parse_file(stem, text):
  """Return {tag label: (speaker, place, date)} of a notebook."""
  talks = {}
  for match in SECTION.finditer(text):
    label = re.sub(r"[%\s]", "", match.group(1))
    fields = {key: [] for key in KEYS}
    for line in match.group(2).splitlines():
      key, _, value = line[3:].partition(":")
      if key in fields and value.strip():
        fields[key].append(value.strip())
    values = tuple(" ".join(fields[key]) for key in KEYS)
    if any(values):
      talks[stem + "-" + label] = values
  return talks


@lru_cache(maxsize=1)
def load_talks():
  talks = {}
  for path in sorted(ROOT.glob("*.tex")):
    text = path.read_text(encoding="utf-8", errors="replace")
    if "\n%% speaker:" in text or "\n%% place:" in text or "\n%% date:" in text:
      talks.update(parse_file(path.stem, text))
  return talks


MONTHS = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]


def date_key(date):
  """Sort key of a date such as "3 December 2026", "September 12, 2024"
  or "September 2024". A date without a year ("In preparation") counts
  as later than every dated one."""
  year, month, day = 9999, 0, 0
  for word in date.replace(",", " ").split():
    if word.lower() in MONTHS:
      month = MONTHS.index(word.lower()) + 1
    elif word.isdigit() and len(word) == 4:
      year = int(word)
    elif word.isdigit():
      day = int(word)
  return (year, month, day)


def latest_talk(notebook):
  """Sort key of the latest dated talk of a notebook; (0, 0, 0) if none."""
  keys = [date_key(values[2]) for label, values in load_talks().items()
          if label.startswith(notebook + "-") and values[2]]
  return max([key for key in keys if key[0] != 9999], default=(0, 0, 0))


def describe(values):
  """One line: speaker. place. date."""
  return ". ".join(value.rstrip(".") for value in values if value) + "."


def annotate(tree):
  """Set .talk on the tags of a tree that have a recorded talk."""
  talks = load_talks()
  for tag in tree or []:
    values = talks.get(tag.label)
    tag.talk = describe(values) if values else None
    if hasattr(tag, "children"):
      annotate(tag.children)
