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
  the page `/talks` (formerly `/slides`), with a link to its PDF and to its TeX source. The
  deployment runs this step and does not fail if a deck fails to build: the
  page then shows that deck without a PDF link.
- To publish a new deck, add it to `slides/index.json`. The manifest is one
  list: an entry is a deck (`path` is `<series>/<deck>`) or a group with a
  `title` and a list `decks`. The page `/talks` is that list and nothing
  else. Keep it that way: simple, just a list, provide the data.
- A deck may list interactive HTML pages under `models` in
  `slides/index.json` (`file`, and a `title` if it should be linked from
  `/talks`). They live in the deck folder, are self-contained, and are
  served as `/talks/<series>/<deck>/<file>`.
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

`huybrechts-reading-seminar/` (beamer deck and notes, copied from `danimalabares/tmp`, `reading-seminar/`, on 18 November 2026) is a silent series: it is not in `index.json`, so it is not built or shown on the website.

The `dbar-poincare` decks were copied from `danimalabares/tmp`, whose `dbar-poincare/` folder was deleted on 18 November 2026 after its README was moved to `slides/dbar-poincare/README.md`.

The Kodaira decks were developed in
`danimalabares/tmp` (`kodaira-lectures/`; that repository was deleted and recreated empty on 18 November 2026, so its old history and links no longer exist)
and copied here on 16 November 2026 from tmp commit `ad55fbd`; lecture 24
slide 12 was edited here afterwards. On 17 November 2026 the drafts, speaker
notes (`notes.md`, `lecture-24-backup.tex`, `lecture-24-appendix.tex`),
`sources.md`, `english-exam/` and `archive/` were copied to
`kodaira-lectures/` in this repository. They are not in `index.json`, so
they are not on the website. Misha's course PDFs (`misha/` in tmp) are not
here, since they are third-party material; they are in the local library
`~/books/people/misha/` (`hodge-theory-2025/`, `hodge-theory-2026/`).
