#!/usr/bin/env python3

import re
import sys
from pathlib import Path


FILES = [
    "differential-geometry.tex",
    "algebraic-geometry.tex",
    "complex-geometry.tex",
    "ringed-spaces.tex",
    "physics.tex",
]


def chapter_title(lines, fallback):
    for index, line in enumerate(lines):
        if not line.lstrip().startswith("\\title{"):
            continue
        title_lines = [line]
        while "}" not in title_lines[-1] and index + 1 < len(lines):
            index += 1
            title_lines.append(lines[index])
        title = "".join(title_lines)
        match = re.search(r"\\title\{(.*?)\}", title, re.S)
        if match:
            return " ".join(match.group(1).split())
    return fallback.replace("-", " ").title()


def preamble():
    lines = Path("preamble.tex").read_text(encoding="utf-8").splitlines(True)
    out = [
        "\\usepackage{amsmath}\n",
        "\\usepackage{amssymb}\n",
        "\\usepackage{amsthm}\n",
    ]

    skip_class = False
    skip_external = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("\\IfFileExists{stacks-project.cls}"):
            skip_class = True
            continue
        if skip_class:
            if stripped == "}":
                skip_class = False
            continue
        if skip_external:
            if "}" in line:
                skip_external = False
            continue
        if stripped.startswith("\\externaldocument"):
            if not stripped.rstrip().endswith("}"):
                skip_external = True
            continue
        out.append(line)
    return "".join(out)


def body_for(filename):
    prefix = filename.removesuffix(".tex")
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    title = chapter_title(lines, prefix)
    out = [
        f"\\chapter{{{title}}}\n",
        f"\\label{{chapter-{prefix}}}\n\n",
    ]

    inside = False
    for line in lines:
        stripped = line.strip()
        if "\\begin{document}" in line:
            inside = True
            continue
        if "\\end{document}" in line:
            break
        if not inside:
            continue
        if stripped.startswith("\\title"):
            continue
        if stripped.startswith("\\maketitle"):
            continue
        if stripped.startswith("\\tableofcontents"):
            continue
        if stripped.startswith("\\phantomsection"):
            continue
        if stripped == "\\label{section-phantom}":
            continue
        if stripped.startswith("\\bibliography"):
            continue
        if stripped.startswith("\\bibliographystyle"):
            continue
        out.append(line)

    return "".join(out)


out = sys.stdout
out.write("\\documentclass{book}\n")
out.write(preamble())
out.write("\n")
out.write("\\begin{document}\n\n")
out.write("\\tableofcontents\n\n")

for filename in FILES:
    out.write(f"% --- Begin {filename} ---\n")
    out.write(body_for(filename))
    out.write(f"% --- End {filename} ---\n\n")

out.write("\\bibliographystyle{alpha}\n")
out.write("\\bibliography{my}\n\n")
out.write("\\end{document}\n")
