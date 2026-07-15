#!/usr/bin/env python3

import runpy
import shutil
import sys

from plasTeX.Context import ContextItem
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


def main():
  plastex = shutil.which("plastex")
  if plastex is None:
    raise SystemExit("plastex executable not found")

  ContextItem.__getitem__ = context_item_getitem
  Gerby.partsList = parts_list
  sys.argv[0] = plastex
  runpy.run_path(plastex, run_name="__main__")


if __name__ == "__main__":
  main()
