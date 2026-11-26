# AGENTS.md

Repository guidance for AI agents working in
this repo. Follow these rules when
editing any heap-project file.

## Public and professional: read this first

The Heap Project is a public website and a
public repository. Write every line as if the
most serious researchers in the field, the
people named in it, and students will read it
at any time. This rule comes before every
other rule in this file and applies to every
AI agent and every session. When in doubt,
leave it out and ask Daniel.

The Heap is a general knowledge notebook. It
is not a diary, not a research journal, not a
chat log, and it is not addressed to Daniel.

Daniel has explicitly made two chapter-level
exceptions to the public-and-professional rule:
`philosophy.tex` and `genealogia-familiar.tex`
may retain their existing personal, informal,
autobiographical, family and other sensitive
material. This exception applies only to those
two chapters and must not be generalized to
other files.

Never publish, in a chapter, a comment, a
template, a slide, a README, a handoff note or
a commit message:

- Personal or private matters of Daniel:
  health, mood, relationships, family, money,
  religion or other practice as his own
  experience, job search, career plans,
  nationality or visa questions, what he
  attended, missed, understood or did not
  understand.
- Private data or anecdotes about other
  people: family members, friends, classmates,
  teachers, colleagues. No private messages,
  no reported conversations, no "X told me",
  no opinions about a person, a talk, a paper
  or an institution, no gossip, no jokes about
  anyone.
- Unpublished work, ideas, plans or career
  facts of other people, including what a
  speaker said aloud but did not put on the
  slides or in a paper. Attribute mathematics
  to published sources.
- The fact that a talk or a class was recorded,
  transcribed or photographed, and any file
  name, timestamp or tool from that pipeline.
  Write "Notes from the talk" or "Notes from
  the lecture of DATE".
- Other people's texts copied at length:
  course notes, essays, summaries received
  privately, book passages, images under
  copyright. Summarise and cite. Daniel alone
  decides exceptions (his own theses are one).
- AI chatter: prompts, "Daniel's question",
  "Editorial answer", "I (Claude)", "ChatGPT
  says", "AI-generated section", speculation
  about what a speaker will say, advice
  addressed to Daniel. If AI assistance must
  be disclosed, use one neutral sentence:
  "drafted with AI assistance; not
  independently checked".
- Diary voice and informal asides: dates of
  personal visits, "during the visit", "my
  laptop", "I couldn't follow", "Yikes",
  "boring", "stupid", "terrible", exclamation
  marks, to-do notes to self. An honest
  mathematical caveat is fine in neutral
  words: "Not checked."
- Coursework as such: answered exams, graded
  homework, question sheets, team essays.
- Unverified statements of fact, and health or
  medical claims.
- Local paths, private links (Drive, Overleaf,
  Zoom, WhatsApp), contact data of others,
  credentials, deployment details.

Rules of procedure:

- Raw material that contains any of the above
  (recordings, transcripts, messages, personal
  notes, coursework) stays outside this
  repository. Only the cleaned, impersonal
  result enters a chapter.
- Session notes and handoff files are not
  tracked here (`notes/` is ignored). Do not
  add them back, and write commit messages
  that could be read by anyone.
- Before every commit that touches text, read
  the diff once only for this rule. Before
  publishing a new chapter or a new section in
  the humanities, on a person, or built from a
  talk, a course or a conversation, check it
  against the list above line by line.
- If existing text breaks this rule, fix it in
  the same session and tell Daniel.
- Deleting from the repository does not delete
  from its history. Sensitive text must never
  be committed in the first place.

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
of Parts XII and XIII, such as
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
