#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


DEFAULT_FILES = ["complex-geometry.tex"]
KNOWN_CHAPTERS = {
    "basic-math",
    "algebra",
    "commutative-algebra",
    "number-theory",
    "differential-geometry",
    "differential-topology",
    "algebraic-geometry",
    "algebraic-topology",
    "categories",
    "infty-categories",
    "complex-analysis",
    "complex-geometry",
    "symplectic-geometry",
    "lie-algebras",
    "representation-theory",
    "vertex-algebras",
    "homological-algebra",
    "deformations",
    "physics",
    "seminars",
    "surfaces",
    "mumford-tate-groups-in-hodge-theory",
    "birational-maps-commutative-algebra",
    "cremona-transformations",
}


def chapter_title(lines, fallback):
    for line in lines:
        match = re.search(r"\\title\{([^}]*)\}", line)
        if match:
            return match.group(1)
    return fallback.replace("-", " ").title()


def should_prefix_ref(label):
    return not any(label.startswith(f"{chapter}-") for chapter in KNOWN_CHAPTERS)


def safe_label(label):
    label = label.strip()
    label = re.sub(r"[^0-9A-Za-z:-]+", "-", label)
    label = re.sub(r"-+", "-", label)
    return label.strip("-")


def prefix_labels_and_refs(line, prefix, label_counts):
    def label_repl(match):
        label = safe_label(f"{prefix}-{match.group(1)}")
        label_counts[label] = label_counts.get(label, 0) + 1
        if label_counts[label] > 1:
            label = f"{label}-duplicate-{label_counts[label]}"
        return f"\\label{{{label}}}"

    line = re.sub(r"\\label\{([^}]*)\}", label_repl, line)

    def ref_repl(match):
        label = match.group(2)
        if should_prefix_ref(label):
            label = f"{prefix}-{label}"
        return f"\\{match.group(1)}{{{safe_label(label)}}}"

    return re.sub(r"\\(ref|eqref)\{([^}]*)\}", ref_repl, line)


def is_sectioning_command(line):
    stripped = line.lstrip()
    return stripped.startswith(("\\section", "\\subsection", "\\subsubsection"))


def preamble():
    lines = Path("preamble.tex").read_text(encoding="utf-8").splitlines(True)
    out = [
        "\\documentclass{report}\n",
        "\\usepackage{amsmath}\n",
        "\\usepackage{amssymb}\n",
        "\\usepackage{amsthm}\n",
    ]

    skip_class = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("\\IfFileExists{stacks-project.cls}"):
            skip_class = True
            continue
        if skip_class:
            if stripped == "}":
                skip_class = False
            continue
        if stripped.startswith("\\externaldocument"):
            continue
        out.append(line)
    return "".join(out)


def body_for(filename):
    path = Path(filename)
    prefix = path.stem
    content = path.read_text(encoding="utf-8")
    content = re.sub(r"\\label\{([^}]*)\}", lambda match: "\\label{" + " ".join(match.group(1).split()) + "}", content)
    lines = content.splitlines(True)
    title = chapter_title(lines, prefix)

    out = [
        f"\\chapter{{{title}}}\n",
        f"\\label{{chapter-{prefix}}}\n\n",
    ]
    inside = False
    label_counts = {}
    seen_section = False
    skip_github_href = False
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
        if is_sectioning_command(line):
            seen_section = True
        if not seen_section:
            if skip_github_href:
                if "github.com/danimalabares" in line and "}" in line:
                    skip_github_href = False
                continue
            if line.lstrip().startswith(r"\href{http://github.com/danimalabares"):
                skip_github_href = True
                if out and out[-1].strip() in (r"\hfill", r"\hfill Notes at"):
                    out.pop()
                if "{github.com/danimalabares" in line and line.rstrip().endswith("}"):
                    skip_github_href = False
                continue
        out.append(prefix_labels_and_refs(line, prefix, label_counts))
    return "".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", default=DEFAULT_FILES)
    args = parser.parse_args()

    print(preamble(), end="")
    print("\\begin{document}\n")
    print("\\tableofcontents\n")
    for filename in args.files:
        print(f"% --- Begin {filename} ---")
        print(body_for(filename), end="")
        print(f"% --- End {filename} ---\n")
    print("\\bibliographystyle{amsalpha}")
    print("\\bibliography{my}")
    print("\\end{document}")


if __name__ == "__main__":
    main()
