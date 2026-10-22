#!/usr/bin/env python3

import runpy
import shutil
import sys

from plasTeX.Base.LaTeX.Verbatim import verbatim
from plasTeX.Context import ContextItem
from plasTeX.Packages import fancyvrb
from plasTeX.Renderers import Gerby

try:
  import jinja2
except ImportError:
  jinja2 = None
else:
  if not hasattr(jinja2, "contextfunction"):
    jinja2.contextfunction = jinja2.pass_context


def context_item_getitem(context, key):
  seen = set()
  while context is not None:
    identifier = id(context)
    if identifier in seen:
      break
    seen.add(identifier)

    try:
      return dict.__getitem__(context, key)
    except KeyError:
      parent = context.parent
      if parent is context:
        break
      context = parent

  raise KeyError(key)


def parts_list(document):
  """Associate chapters with preceding parts."""
  parts = {}
  current = None
  stack = list(reversed(document.childNodes))

  while stack:
    node = stack.pop()
    if node.nodeName == "part":
      current = node.ref.source
      parts[current] = []
    elif (
      node.nodeName == "chapter"
      and current is not None
    ):
      parts[current].append(node.ref.source)
    stack.extend(reversed(node.childNodes))

  return parts


# fancyvrb calls strip() on these values.
FANCYVRB_TEXT_OPTIONS = (
  "frame",
  "framerule",
  "framesep",
  "fontfamily",
  "fontsize",
  "fontseries",
  "fontshape",
)


class FancyvrbVerbatim:
  """Name macro values such as \\footnotesize."""

  @staticmethod
  def parse(node, tex):
    result = verbatim.parse(node, tex)
    options = node.attributes.get("options")
    for key in FANCYVRB_TEXT_OPTIONS:
      value = (options or {}).get(key)
      if value is not None and not hasattr(
        value, "strip"
      ):
        options[key] = value.nodeName
    return result


def main():
  plastex = shutil.which("plastex")
  if plastex is None:
    raise SystemExit("plastex executable not found")

  ContextItem.__getitem__ = context_item_getitem
  Gerby.partsList = parts_list
  # fancyvrb.Verbatim.parse calls this name.
  fancyvrb.verbatim = FancyvrbVerbatim
  # plasTeX imports packages by short name.
  sys.modules["fancyvrb"] = fancyvrb
  sys.argv[0] = plastex
  runpy.run_path(plastex, run_name="__main__")


if __name__ == "__main__":
  main()
