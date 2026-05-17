#!/usr/bin/env python3

import runpy
import shutil
import sys

try:
  import jinja2
except ImportError:
  jinja2 = None
else:
  if not hasattr(jinja2, "contextfunction"):
    jinja2.contextfunction = jinja2.pass_context


def main():
  plastex = shutil.which("plastex")
  if plastex is None:
    raise SystemExit("plastex executable not found")

  sys.argv[0] = plastex
  runpy.run_path(plastex, run_name="__main__")


if __name__ == "__main__":
  main()
