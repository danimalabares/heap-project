---
name: heap-project-chapter
description: Create and fully register a new Heap Project notebook or chapter, including its standalone TeX file, combined-book and Gerby integration, and two-letter shell aliases. Use when the user asks to start, add, or create an HP subject or chapter; do not use merely to edit an existing chapter.
---

# Heap Project chapter creation

Create the chapter in the Heap Project and
the matching alias packet in
`~/github/config/aliases.sh`.

## Before editing

1. Work from the Heap Project repository
   root and read its `AGENTS.md` completely.
2. Inspect `git status --short --branch` in
   both `~/github/heap-project` and
   `~/github/config`. Preserve all unrelated
   work. Do not commit or push unless the
   user explicitly requests it.
3. Resolve these values:
   - display title;
   - lowercase kebab-case filename stem;
   - destination Part title and, if the Part
     is new, its Roman numeral;
   - an unused two-letter lowercase code.
4. Infer an obvious code when it is unique.
   Ask only when the code is ambiguous or
   collides with an existing mapping or
   alias.

## Create and register

Run the bundled deterministic editor:

```sh
hp_root="$(git rev-parse --show-toplevel)"
python3 \
  "$hp_root/.agents/skills/heap-project-chapter/scripts/create_hp_chapter.py" \
  --title "TITLE" \
  --slug "SLUG" \
  --code "CODE" \
  --part-title "PART TITLE" \
  --part-number "ROMAN"
```

Omit `--part-number` when the requested Part
already exists. Use `--config` only if the
config repository is not at the default
location.

The script must leave all of these consistent:

- `<slug>.tex` as a standalone HP document;
- `GERBY_FILES` in `Makefile`;
- chapter and Part placement in
  `order-chapters.txt`;
- the cross-document entry in `preamble.tex`;
- `KNOWN_CHAPTERS` in
  `scripts/make_gerby_book.py`;
- the `hp_file` map, `hplist`, and the
  `vCODE`/`pCODE`/`cCODE` alias block in
  `~/github/config/aliases.sh`.

Do not edit generated `book.tex`, `gerby/`,
`tmp/`, PDFs, or LaTeX build artifacts.

## Verify

Inspect both diffs and run:

```sh
latexmk -pdf -interaction=nonstopmode \
  -halt-on-error "SLUG.tex"
make gerby-book
zsh -n ~/github/config/aliases.sh
zsh -f -c \
  'source ~/github/config/aliases.sh; hp_file CODE'
git diff --check
git -C ~/github/config diff --check
```

Confirm that the generated `gerby/book.tex`
contains the requested Part and chapter, and
that `hp_file CODE` prints exactly the slug.
Report the files changed and verification
results. Clean only ignored build products
created by this run; never discard tracked or
unrelated user changes.
