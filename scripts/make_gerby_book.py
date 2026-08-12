#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path


DEFAULT_FILES = ["complex-geometry.tex"]
KNOWN_CHAPTERS = {
    "basic-math",
    "algebra",
    "commutative-algebra",
    "differential-geometry",
    "differential-topology",
    "algebraic-geometry",
    "algebraic-topology",
    "categories",
    "infty-categories",
    "complex-analysis",
    "complex-geometry",
    "hodge-theory",
    "k3",
    "ringed-spaces",
    "schemes",
    "symplectic-geometry",
    "lie-algebras",
    "representation-theory",
    "vertex-algebras",
    "homological-algebra",
    "deformations",
    "physics",
    "probability",
    "economy",
    "seminars",
    "geometric-prequantization",
    "surfaces",
    "stanley-reisner",
    "mumford-tate-groups-in-hodge-theory",
    "birational-maps-commutative-algebra",
    "cremona-transformations",
}


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


def should_prefix_ref(label):
    return not any(label.startswith(f"{chapter}-") for chapter in KNOWN_CHAPTERS)


def safe_label(label):
    label = label.strip()
    label = re.sub(r"[^0-9A-Za-z:-]+", "-", label)
    label = re.sub(r"-+", "-", label)
    return label.strip("-")


def normalize_title(title):
    title = title.strip().lower()
    title = title.replace("&", "and")
    return re.sub(r"[^0-9a-z]+", " ", title).strip()


def part_label(entry):
    return safe_label(f"part-{normalize_title(entry)}")


def order_entries(order_path):
    if not order_path:
        return []

    path = Path(order_path)
    if not path.exists():
        print(
            f"warning: order file not found: {order_path}",
            file=sys.stderr,
        )
        return []

    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.fullmatch(r"PART\s+[IVXLCDM]+\s*:\s*(.+)", stripped)
        if match:
            entries.append(("part", match.group(1)))
        else:
            entries.append(("chapter", stripped))
    return entries


def ordered_files(files, order_path):
    if not order_path:
        return files

    entries = [
        entry
        for kind, entry in order_entries(order_path)
        if kind == "chapter"
    ]
    by_title = {}
    for filename in files:
        source = Path(filename)
        if not source.exists():
            continue
        lines = source.read_text(encoding="utf-8").splitlines(True)
        title = chapter_title(lines, source.stem)
        keys = {
            normalize_title(title),
            normalize_title(source.stem),
            normalize_title(source.stem.replace("-", " ")),
        }
        for key in keys:
            by_title.setdefault(key, filename)

    ordered = []
    used = set()
    for entry in entries:
        key = normalize_title(entry)
        filename = by_title.get(key)
        if not filename:
            print(
                f"warning: no Gerby source matches "
                f"order-chapters entry: {entry}",
                file=sys.stderr,
            )
            continue
        if filename in used:
            continue
        ordered.append(filename)
        used.add(filename)

    ordered.extend(filename for filename in files if filename not in used)
    return ordered


def prefix_labels_and_refs(line, prefix, label_counts):
    def label_repl(match):
        raw_label = match.group(1)
        if should_prefix_ref(raw_label):
            label = safe_label(f"{prefix}-{raw_label}")
        else:
            label = safe_label(raw_label)
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
        "\\documentclass{book}\n",
        "\\usepackage{amsmath}\n",
        "\\usepackage{amssymb}\n",
        "\\usepackage{amsthm}\n",
    ]

    skip_class = False
    skip_external = 0
    for line in lines:
        stripped = line.strip()
        if skip_external:
            skip_external += line.count("{")
            skip_external -= line.count("}")
            continue
        if stripped.startswith("\\IfFileExists{stacks-project.cls}"):
            skip_class = True
            continue
        if skip_class:
            if stripped == "}":
                skip_class = False
            continue
        if not stripped or stripped.startswith("%"):
            out.append(line)
            continue
        if stripped.startswith("\\usepackage{xr-hyper}"):
            continue
        if stripped.startswith("\\usepackage{multicol}"):
            continue
        if stripped.startswith(
            "\\newcommand{\\maybeexternaldocument}"
        ) or stripped.startswith(
            "\\renewcommand{\\externaldocument}"
        ):
            skip_external = line.count("{") - line.count("}")
            continue
        if stripped.startswith("\\maybeexternaldocument"):
            skip_external = line.count("{") - line.count("}")
            continue
        if stripped.startswith("\\externaldocument"):
            skip_external = line.count("{") - line.count("}")
            continue
        if stripped.startswith("\\let\\externaldocumentorig\\externaldocument"):
            continue
        out.append(line)
    return "".join(out)


def body_for(filename):
    path = Path(filename)
    prefix = path.stem
    content = path.read_text(encoding="utf-8")
    content = re.sub(r"\\mathbb\{([^{}]+)\}", r"\1", content)
    content = re.sub(r"\\text\{([^{}]+)\}", r"\1", content)
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
    parser.add_argument(
        "--order",
        help="text file listing chapter titles in TOC order",
    )
    parser.add_argument("files", nargs="*", default=DEFAULT_FILES)
    args = parser.parse_args()
    files = ordered_files(args.files, args.order)
    entries = order_entries(args.order)

    print(preamble(), end="")
    print("\\begin{document}\n")
    print("\\tableofcontents\n")
    filenames = iter(files)
    next_filename = next(filenames, None)
    for kind, entry in entries:
        if kind == "part":
            print(f"\\part{{{entry}}}")
            print(f"\\label{{{part_label(entry)}}}\n")
            continue
        if not next_filename:
            continue
        print(f"% --- Begin {next_filename} ---")
        print(body_for(next_filename), end="")
        print(f"% --- End {next_filename} ---\n")
        next_filename = next(filenames, None)
    while next_filename:
        print(f"% --- Begin {next_filename} ---")
        print(body_for(next_filename), end="")
        print(f"% --- End {next_filename} ---\n")
        next_filename = next(filenames, None)
    print("\\bibliographystyle{amsalpha}")
    print("\\bibliography{my}")
    print("\\end{document}")


if __name__ == "__main__":
    main()
