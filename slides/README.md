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
`../assets/<file>`. Build one deck with `make <deck>` inside the series
folder, or with `latexmk -pdf <deck>.tex` inside the deck folder.

## Rules

- Slides are not chapters. They are not in `GERBY_FILES`, get no tags, and
  are not part of `book.tex`.
- The chapter style rules of `AGENTS.md` (no macros, 45-character lines, no
  text in equations) do not apply here. A series may define its own macros
  in its `preamble.tex`.
- Compiled PDFs are not committed (`*.pdf` is ignored). Images are.
- Give every image a source and licence line on the slide where it appears.
- On slides, cite published sources or the lecturer's own slides, with exact
  slide or section numbers where possible. Mark what was not verified; in the
  Kodaira decks red text means "not verified by the speaker".

## Index

| Series | Deck | Occasion |
| --- | --- | --- |
| `kodaira-lectures` | `lecture-23`: Kodaira embedding theorem (Part 1), the mechanism and Nadel's theorem, 61 slides | Seminar on M. Verbitsky's Hodge theory course (IMPA 2025), November 2026 |
| `kodaira-lectures` | `lecture-24`: Kodaira embedding theorem (Part 2), embedding, Chow, Kawamata–Viehweg, 60 slides | Same seminar, 16 November 2026 |

The Kodaira decks were developed in
[danimalabares/tmp](https://github.com/danimalabares/tmp/tree/main/kodaira-lectures),
which also holds the drafts, speaker notes and source list. They were copied
here on 16 November 2026 from tmp commit `ad55fbd`.
