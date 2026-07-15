#!/usr/bin/env python3

import runpy
import shutil
import sys

from plasTeX.Context import ContextItem

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


def main():
  plastex = shutil.which("plastex")
  if plastex is None:
    raise SystemExit("plastex executable not found")

  ContextItem.__getitem__ = context_item_getitem
  sys.argv[0] = plastex
  runpy.run_path(plastex, run_name="__main__")


if __name__ == "__main__":
  main()
