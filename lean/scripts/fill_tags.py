#!/usr/bin/env python3
"""Replace @label@ placeholders in a Lean file by 'TAG (label)'.

Usage: fill_tags.py CHAPTER FILE.lean
Looks up CHAPTER-label in ../registry/tags (relative to lean/).
"""
import re, sys, pathlib
chapter, path = sys.argv[1], pathlib.Path(sys.argv[2])
root = pathlib.Path(__file__).resolve().parents[2]
tags = {}
for line in (root / "registry" / "tags").read_text().splitlines():
    if line.startswith("#") or "," not in line:
        continue
    tag, name = line.split(",", 1)
    tags[name] = tag
def sub(m):
    key = f"{chapter}-{m.group(1)}"
    if key not in tags:
        sys.exit(f"no tag for {key}")
    return f"{tags[key]} ({m.group(1)})"
s = path.read_text()
path.write_text(re.sub(r"@([A-Za-z0-9\[\]-]+)@", sub, s))
