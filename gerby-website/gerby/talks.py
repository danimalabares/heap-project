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
