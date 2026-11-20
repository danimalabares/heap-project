# AGENTS.md

Repository guidance for AI agents working in
this repo. Follow this rules when
editing any heap-project file!!!!

- Do not use any macros at all.
- Do not write text in equations.
  Write in prose whatever you need to explain
  and put only formulas in equations.
- Put standalone formulas and diagrams in
  display math, using `$$ ... $$` or an
  equation environment. Single-dollar math
  stays inline even on separate source lines.
  Keep short symbols within sentences inline.

- Do not use `align*`. For unnumbered aligned displays, use:

  ```tex
  $$
  \begin{aligned}
  A &= B \\
    &= C
  \end{aligned}
  $$
  ```

- For numbered aligned displays, use:

  ```tex
  \begin{equation}
  \begin{aligned}
  A &= B \\
    &= C
  \end{aligned}
  \end{equation}
  ```

- Maximum linewidth is 45 characters.
- Use `\mathbb{Z}`, `\mathbb{R}`, and
  `\mathbb{C}` for the integers, real
  numbers, and complex numbers,
  respectively.
- Do not write inner products with raw 
  angle brackets like `\left< X,Y \right>`. 
  Use `\left\langle{} X,Y \right\rangle{}` 
  instead.
- Do not use `\subsetneq`; use `\subset` 
- instead.
- Do not use `\supsetneq`; use `\supset` 
  instead.
- In every `definition` environment, 
  italicize the term being defined.
- Write recalled definitions as prose, not in
  a `definition` environment. Reserve that
  environment for definitions introduced here.
- Write corollaries in the `corollary`
  environment. It shares its numbering
  with theorems, lemmas, and propositions.
  Do not use `\begin{lemma}[Corollary]`.
  Use the optional title only for extra
  information, as in
  `\begin{corollary}[Yau's conjecture]`.
- Do not rename labels when changing the
  environment type of a statement. Keep
  labels like `\label{lemma-foo}` as they
  are, since the permanent tags follow them.
- When changing an environment type, also
  fix references written in prose such as
  `Lemma~\ref{lemma-foo}`.
- Never use capital letters in LaTeX labels. Use labels like
  `\label{theorem-rauch-clean}` instead of
  `\label{theorem-Rauch-clean}` or
  `\label{section-Hadamard}`. This applies 
  to theorem, lemma,
  proposition, definition, equation, 
  exercise, section, and remark labels.
- Do not globally reformat existing TeX 
  files. Preserve the repo's line wrapping 
  and style.
- Before committing TeX cleanup changes, 
  check that no source `.tex` files contain 
  `\begin{align*}`, `\end{align*}`, 
  `\left<`, or `\right>` outside generated 
  directories like `gerby/` and `tmp/`.
- Do not use subsections or subsubsections.

## Slides

Beamer decks live in `slides/`, one folder per
talk or series; see `slides/README.md`.
They are not chapters: do not add them to
`GERBY_FILES`, and the style rules above
(no macros, 45-character lines, no text in
equations) do not apply inside `slides/`.
Decks listed in `slides/index.json` are
published on the website at `/talks`.

Generated files and directories such as
`gerby/`, `tmp/`, `.venv/`, and build
artifacts should not be committed.

## Standalone documents

`standalone/` keeps older documents as
originals: the PDF as `standalone/NAME.pdf`
and its TeX, bibliography and figures in
`standalone/sources/NAME/`. They are not
chapters. Keep them verbatim: the style rules
above (no macros, 45-character lines, no text
in equations) and bulk cleanups such as
`scripts/gerby_align_cleanup.py` do not apply
there. Only fix what is needed to compile.
Question sheets and other course handouts do
not belong here; they live in the Drive
coursework folder.

## Talks in seminar notebooks

Every section of a seminar or conference
notebook that records one talk (the notebooks
of Parts XI and XII, such as
`seminars-algebra.tex`) gives the speaker,
place and date in comment lines right after
its `\label`:

```
%% speaker: Name, Affiliation
%% place: Seminar, Institution
%% date: September 12, 2024
```

Plain text, no TeX markup. Omit a line when
the fact is not known; never guess it. A long
value continues on further lines with the
same key. The website shows them under the
title of the section in the table of
contents (`gerby-website/gerby/talks.py`), and
`scripts/test_gerby_routes.py` checks that
the seminar notebooks record one for every
section.

## Commit provenance

Every commit containing AI-generated or AI-edited content must make the AI involvement explicit in the commit message. Name the AI/tool responsible (for example, `ChatGPT:` or `Claude:`) and briefly describe what it changed. For substantial automation, make the extent of the automated work clear enough for later debugging and provenance tracking.

## Permanent Gerby tags

- After adding or renaming a `\label` in a
  Gerby chapter, run `make gerby-register`.
  Commit `registry/tags` and any new
  `registry/snapshots/*.tags` with the
  change. Builds never allocate tags.
- Labels within a chapter must be unique.
- Never edit, delete, or regenerate
  `registry/history.json`, the files it
  lists, or `registry/snapshots/`.
- To keep a tag across a label rename, add
  the old-to-new pair to
  `scripts/gerby_label_migrations.json`
  before registering, and only if both
  labels denote the same object.
