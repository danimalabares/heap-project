#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


def fail(message):
    raise SystemExit(message)


def normalized(text):
    return " ".join(text.lower().split())


def replace_once(text, old, new, description):
    count = text.count(old)
    if count != 1:
        fail(
            f"expected one {description} marker, "
            f"found {count}"
        )
    return text.replace(old, new, 1)


def update_makefile(text, tex_name):
    match = re.search(r"^GERBY_FILES \?= (.+)$", text, re.M)
    if not match:
        fail("GERBY_FILES was not found in Makefile")
    files = match.group(1).split()
    if tex_name in files:
        fail(f"{tex_name} is already in GERBY_FILES")
    replacement = match.group(0) + " " + tex_name
    return text[: match.start()] + replacement + text[match.end() :]


def update_order(text, title, part_title, part_number):
    lines = text.splitlines()
    part_re = re.compile(r"^PART ([IVXLCDM]+):\s*(.+)$")

    for line in lines:
        match = part_re.fullmatch(line.strip())
        if not match and normalized(line) == normalized(title):
            fail(f"chapter title already appears in order file: {title}")

    headers = []
    for index, line in enumerate(lines):
        match = part_re.fullmatch(line.strip())
        if match:
            headers.append((index, match.group(1), match.group(2)))

    chosen = None
    for header in headers:
        if normalized(header[2]) == normalized(part_title):
            chosen = header
            break

    if chosen is None:
        if not part_number:
            fail("--part-number is required for a new Part")
        if not re.fullmatch(r"[IVXLCDM]+", part_number):
            fail("Part number must be an uppercase Roman numeral")
        if any(number == part_number for _, number, _ in headers):
            fail(f"Part {part_number} already has another title")
        result = text.rstrip()
        return (
            result
            + f"\n\nPART {part_number}: {part_title}\n\n"
            + title
            + "\n"
        )

    start = chosen[0]
    end = len(lines)
    for index, _, _ in headers:
        if index > start:
            end = index
            break

    insert_at = end
    while insert_at > start and not lines[insert_at - 1].strip():
        insert_at -= 1
    lines[insert_at:insert_at] = ["", title]
    return "\n".join(lines).rstrip() + "\n"


def update_preamble(text, slug):
    entry = f"\\externaldocument[{slug}-]{{{slug}}}"
    if entry in text:
        fail(f"preamble already contains {entry}")
    marker = "\n% Theorem environments."
    return replace_once(
        text,
        marker,
        "\n" + entry + "\n" + marker,
        "theorem-environments",
    )


def update_known_chapters(text, slug):
    match = re.search(r"KNOWN_CHAPTERS = \{\n(.*?)\n\}", text, re.S)
    if not match:
        fail("KNOWN_CHAPTERS was not found")
    body = match.group(1)
    if re.search(rf'^\s+"{re.escape(slug)}",$', body, re.M):
        fail(f"KNOWN_CHAPTERS already contains {slug}")
    replacement = body + f'\n    "{slug}",'
    return text[: match.start(1)] + replacement + text[match.end(1) :]


def update_aliases(text, title, slug, code):
    alias_names = [f"v{code}", f"p{code}", f"c{code}"]
    if re.search(rf"^\s+{re.escape(code)}\)", text, re.M):
        fail(f"Heap Project code already exists: {code}")
    if re.search(rf"^{re.escape(code)}\s+", text, re.M):
        fail(f"hplist code already exists: {code}")
    for alias_name in alias_names:
        if re.search(rf"^alias {re.escape(alias_name)}=", text, re.M):
            fail(f"alias already exists: {alias_name}")

    hp_file_start = text.find("hp_file() {")
    hp_file_end = text.find("\n}\n\nhp_tex()", hp_file_start)
    if hp_file_start < 0 or hp_file_end < 0:
        fail("hp_file function boundaries were not found")
    hp_file = text[hp_file_start:hp_file_end]
    hp_file = replace_once(
        hp_file,
        "    *)\n",
        f"    {code}) printf '%s\\n' '{slug}' ;;\n    *)\n",
        "hp_file fallback",
    )
    text = text[:hp_file_start] + hp_file + text[hp_file_end:]

    hplist_start = text.find("hplist() {")
    hplist_end = text.find("\nEOF\n}", hplist_start)
    if hplist_start < 0 or hplist_end < 0:
        fail("hplist boundaries were not found")
    text = (
        text[:hplist_end]
        + f"\n{code}  {slug}"
        + text[hplist_end:]
    )

    block = (
        f"# {title} ({code}) {{{{{{3\n"
        f"# HP file: {slug}.tex\n"
        f"alias v{code}='hpv {code}'\n"
        f"alias p{code}='hpp {code}'\n"
        f"alias c{code}='hpc {code}'\n\n"
        "# Related non-HP aliases can go here.\n"
        "# }}}\n"
    )
    marker = "# }}}\n# Other math aliases {{{2"
    return replace_once(
        text,
        marker,
        block + marker,
        "Heap Project subjects closing",
    )


def chapter_template(title):
    return f"""\\input{{preamble}}

\\begin{{document}}

\\title{{{title}}}
\\maketitle

\\phantomsection
\\label{{section-phantom}}

\\tableofcontents



\\bibliography{{my}}
\\bibliographystyle{{amsalpha}}

\\end{{document}}
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--code", required=True)
    parser.add_argument("--part-title", required=True)
    parser.add_argument("--part-number")
    parser.add_argument("--repo", default=".")
    parser.add_argument(
        "--config",
        default="~/github/config/aliases.sh",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        fail("slug must be lowercase kebab-case")
    if not re.fullmatch(r"[a-z]{2}", args.code):
        fail("code must contain exactly two lowercase letters")
    if any(character in args.title for character in "{}\n"):
        fail("title cannot contain braces or newlines")

    repo = Path(args.repo).expanduser().resolve()
    config = Path(args.config).expanduser().resolve()
    targets = {
        "Makefile": repo / "Makefile",
        "order-chapters.txt": repo / "order-chapters.txt",
        "preamble.tex": repo / "preamble.tex",
        "make_gerby_book.py": repo / "scripts/make_gerby_book.py",
        "aliases.sh": config,
    }
    for name, path in targets.items():
        if not path.is_file():
            fail(f"missing {name}: {path}")

    chapter = repo / f"{args.slug}.tex"
    if chapter.exists():
        fail(f"chapter already exists: {chapter}")

    original = {
        name: path.read_text(encoding="utf-8")
        for name, path in targets.items()
    }
    changed = {
        "Makefile": update_makefile(
            original["Makefile"], f"{args.slug}.tex"
        ),
        "order-chapters.txt": update_order(
            original["order-chapters.txt"],
            args.title,
            args.part_title,
            args.part_number,
        ),
        "preamble.tex": update_preamble(
            original["preamble.tex"], args.slug
        ),
        "make_gerby_book.py": update_known_chapters(
            original["make_gerby_book.py"], args.slug
        ),
        "aliases.sh": update_aliases(
            original["aliases.sh"],
            args.title,
            args.slug,
            args.code,
        ),
    }

    for name, path in targets.items():
        path.write_text(changed[name], encoding="utf-8")
    chapter.write_text(chapter_template(args.title), encoding="utf-8")

    print(f"created {chapter}")
    for path in targets.values():
        print(f"updated {path}")


if __name__ == "__main__":
    main()
