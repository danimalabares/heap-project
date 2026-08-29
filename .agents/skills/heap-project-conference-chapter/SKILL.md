---
name: heap-project-conference-chapter
description: Create and register a new Heap Project conference chapter from an official conference URL, prepopulating Part II with conference metadata and one section per scheduled talk or minicourse. Use when starting a new HP conference notebook; do not use merely to add notes to an existing chapter or for a single seminar talk.
---

# Heap Project conference chapter

Turn the conference's official website into
a ready-to-use HP notebook in Part II.

## Prepare

1. Work from the Heap Project repository
   root and read `AGENTS.md` completely.
2. Read
   [references/conference-format.md](references/conference-format.md)
   completely before collecting data or
   writing TeX.
3. Inspect `git status --short --branch` in
   both the Heap Project and config
   repositories. Preserve unrelated work.
   Do not commit or push unless the user
   explicitly requests it.
4. Require the official conference URL.
   Resolve an unused lowercase kebab-case
   slug and unused two-letter HP code. Infer
   them when unambiguous; ask only if there
   is a collision or a consequential choice.

## Research the official programme

Browse the supplied site and the first-party
pages or files it links. Inspect every day,
track, tab, pagination page, expandable
entry, programme PDF, and abstract page
needed to build the complete academic
programme.

Use official sources only. A page or file on
another institutional domain counts when
the official conference site links to it as
part of the programme. Do not silently fill
gaps from search snippets, social media,
personal pages, or conference aggregators.

Make a source-backed inventory before
editing. Capture:

- official conference title, dates, venue,
  place, organizers, and official URL;
- every scheduled talk, lecture, and
  minicourse;
- for each item, its official type, exact
  title, speaker, affiliation, date, time,
  room or venue, abstract, and entry URL;
- every scheduled session of a minicourse.

Exclude registration, breaks, meals,
ceremonies, and purely social activities.
Treat a multi-session minicourse as one
section with all session times. Treat each
separately titled academic presentation as
its own section.

If the official sources conflict, prefer the
most recently updated official programme
and record the discrepancy in the handoff.
If required content is inaccessible or the
programme cannot be made complete, stop
and ask the user for the missing official
page or file. Never invent missing data.

## Create and populate

First register the chapter with the existing
deterministic editor:

```sh
hp_root="$(git rev-parse --show-toplevel)"
python3 \
  "$hp_root/.agents/skills/heap-project-chapter/scripts/create_hp_chapter.py" \
  --title "OFFICIAL CONFERENCE TITLE" \
  --slug "SLUG" \
  --code "CODE" \
  --part-title \
    "seminars, conferences, minicourses, workshops"
```

Use `--config` only when the config file is
not at `~/github/config/aliases.sh`.

Replace the generated TeX skeleton with the
complete conference notebook described in
the format reference. The chapter must be
useful before any handwritten notes are
added. Keep source order chronological,
including parallel sessions in the order
shown by the official programme.

Abstracts must be verbatim in wording,
punctuation, capitalization, and paragraph
breaks. Do not summarize, translate,
copyedit, silently correct, or complete an
abstract. Only make mechanical changes
needed for valid TeX and the repository's
45-character wrapping. Mark unavailable
fields explicitly as unavailable on the
official site and include the access date.

## Verify

Compare the chapter against the source
inventory. The number and order of sections
must match the included programme items,
and every available abstract must pass a
word-for-word check after ignoring only TeX
escaping and whitespace introduced for line
wrapping.

Run:

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

Confirm that `gerby/book.tex` places the
chapter in Part II and that `hp_file CODE`
prints exactly the slug. Do not commit
generated files or build products.

Report the official sources used, the item
count by type, explicitly unavailable data,
all changed files, and verification results.
