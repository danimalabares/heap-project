# Slides

Beamer decks for talks and seminar lectures. One folder per talk or series.

## Layout

```
slides/
  <series>/
    preamble.tex        shared beamer preamble and macros for the series
    assets/             images used by the decks
    Makefile            `make` builds every deck of the series
    <deck>/<deck>.tex   one folder per deck, same basename as the folder
```

A deck starts with `\input{../preamble.tex}` and refers to images as
`../assets/<file>`. A single talk (series `talks`) may instead keep its own
preamble and images inside its deck folder. Build one deck with `make <deck>` inside the series
folder, or with `latexmk -pdf <deck>.tex` inside the deck folder.

## Rules

- Slides are not chapters. They are not in `GERBY_FILES`, get no tags, and
  are not part of `book.tex`.
- Slides are published on the website. Every deck listed in
  `slides/index.json` is built by `make gerby-slides`
  (`scripts/build_slides.py`) into `gerby/downloads/slides/` and appears on
  the page `/slides`, with a link to its PDF and to its TeX source. The
  deployment runs this step and does not fail if a deck fails to build: the
  page then shows that deck without a PDF link.
- To publish a new deck, add it to `slides/index.json`. The manifest is one
  list: an entry is a deck (`path` is `<series>/<deck>`) or a group with a
  `title` and a list `decks`. The page `/slides` is that list and nothing
  else. Keep it that way: simple, just a list, provide the data.
- Do not name a file `beamer-preamble.tex`: `.gitignore` ignores that name.
  Use `preamble.tex`.
- The chapter style rules of `AGENTS.md` (no macros, 45-character lines, no
  text in equations) do not apply here. A series may define its own macros
  in its `preamble.tex`.
- Compiled PDFs are not committed (`*.pdf` is ignored). Images are.
- Give every image a source and licence line on the slide where it appears.
- On slides, cite published sources or the lecturer's own slides, with exact
  slide or section numbers where possible. Mark what was not verified; in the
  Kodaira decks red text means "not verified by the speaker".

## Index

The list of published decks is `slides/index.json`.

| Series | Decks | Copied from |
| --- | --- | --- |
| `dbar-poincare` | `lecture-12`, `lecture-13` | `danimalabares/tmp`, `dbar-poincare/` |
| `kodaira-lectures` | `plan`, `lecture-23`, `lecture-24` | `danimalabares/tmp`, `kodaira-lectures/` |
| `talks` | `stanley-reisner-opega`, `stanley-reisner-legalzinho` | `danimalabares/daniel`, `others/talks/` |
| `talks` | `nakajima-heisenberg` | `vertex-algebras` repository, `beamer.tex` |

Changes made when copying (16 November 2026): image paths; the spelling
"Stanley-Raisner" corrected to "Stanley-Reisner"; `\date{\today}` in the
Nakajima deck replaced by "November 2025" (from the git history, exact day
of the talk not verified); `link.png` of the OPEGA deck taken from the
Legalzinho folder. Most images in the older decks have no source or licence
line yet.

The Kodaira decks were developed in
[danimalabares/tmp](https://github.com/danimalabares/tmp/tree/main/kodaira-lectures),
which also holds the drafts, speaker notes and source list. They were copied
here on 16 November 2026 from tmp commit `ad55fbd`.
