#!/usr/bin/env python3

import runpy
import shutil
import sys
import base64
import html
import re
from pathlib import Path

from plasTeX.Base.LaTeX.Verbatim import verbatim
from plasTeX.Context import ContextItem
from plasTeX.Packages import fancyvrb
from plasTeX.Renderers import Gerby


def render_source_image(node):
  """Keep supplied PNGs visible in standalone tag HTML."""
  path = Path(node.imageoverride)
  if path.suffix.lower() != ".png":
    raise ValueError("Expected a PNG source figure")
  data = base64.b64encode(path.read_bytes()).decode("ascii")
  options = node.attributes.get("options") or {}
  width = str(options.get("width", ""))
  match = re.fullmatch(
      r"\s*([0-9.]+)\s*\\(?:line|text)width\s*", width
  )
  percent = min(100, max(1, float(match[1]) * 100)) if match else 100
  return (
      '<img src="data:image/png;base64,' + data + '" '
      'alt="' + html.escape(path.stem, quote=True) + '" '
      'style="width:' + str(percent) + '%;max-width:100%;height:auto">'
  )


def install_source_images(renderer_class):
  original = renderer_class.loadTemplates

  def load_templates(self, document):
    original(self, document)
    fallback = self.get("includegraphics")

    def image(node):
      path = getattr(node, "imageoverride", None)
      if path and Path(path).parent.name == "combinatorics-assets":
        return render_source_image(node)
      return fallback(node) if fallback else ""

    self["includegraphics"] = image

  renderer_class.loadTemplates = load_templates

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
  install_source_images(Gerby.Renderer)
  # fancyvrb.Verbatim.parse calls this name.
  fancyvrb.verbatim = FancyvrbVerbatim
  # plasTeX imports packages by short name.
  sys.modules["fancyvrb"] = fancyvrb
  sys.argv[0] = plastex
  runpy.run_path(plastex, run_name="__main__")


if __name__ == "__main__":
  main()
