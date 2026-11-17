# Kodaira lectures

The original nine-slide outline is preserved unchanged in [plan/slides.tex](plan/slides.tex).

| Folder | Draft | Slides |
| --- | --- | ---: |
| [lecture-23](lecture-23/lecture-23.tex) | Embedding mechanism and Nadel vanishing | 61 |
| [lecture-24](lecture-24/lecture-24.tex) | Essential embedding proof; detailed backup retained | 14 working; 54 backup; 32 optional |

These two decks form one continuous argument, with a short course recap and Kodaira embedding as the initial goal. The first lecture explains how H1-vanishing gives values and first jets before developing Nadel. The second recaps the actual lecture 23 recording, resumes with the missing metric construction, and supplies the value/jet argument deferred in class. They follow Daniel's talk checklist: announce the destination, explain the route, carry out the argument, and return to the result. They retain the dbar-poincare Beamer style, use mathematical pictures and short historical pauses, and move longer technical arguments into optional preparation notes. Shared styling is in [preamble.tex](preamble.tex).

## Build

Run from this folder:

```sh
make
```

Or compile an individual deck from its own folder:

```sh
cd lecture-23
pdflatex -interaction=nonstopmode -halt-on-error lecture-23.tex
pdflatex -interaction=nonstopmode -halt-on-error lecture-23.tex
```

For lecture 24, use folder `lecture-24` and source `lecture-24.tex`; for the outline, use folder `plan` and source `slides.tex`. The lecture outputs are `lecture-23/lecture-23.pdf` and `lecture-24/lecture-24.pdf`. Compiled PDFs remain local, following the repository's existing PDF ignore rule.

## Mathematical scope

Lecture 23 opens with two recap slides covering the course from complex structures to singular psh weights. It then states Kodaira embedding, explains why point and tangent separation suffice, and proves the mechanism from the evaluation exact sequence. This motivates the multiplier ideal, the weighted Dolbeault resolution, and the Nadel deduction. Bochner–Kodaira and Kodaira vanishing are brief reminders. The weighted local lemma and singular-weight L2 existence theorem remain explicit analytic inputs. Hahn–Banach, operator domains, and approximation details are optional notes.

Lecture 24 is now an essentials-only working presentation: the vanishing and its analytic mechanism, the global singular metric, values and first jets, embedding, and Chow. The previous detailed 54-slide draft and notes are preserved as lecture-24-backup.tex/pdf and notes-backup.md. The separate optional KV appendix is unchanged.

See [lecture-23/notes.md](lecture-23/notes.md), [lecture-24/notes.md](lecture-24/notes.md), and [sources.md](sources.md). Each notes file starts with the essential preparation, followed by optional details. No “Earlier inputs” footers have been restored. Numbered references to our seminar retain the known speaker's name.

Talk preparation checklist: [HOW TO GIVE A TALK](https://github.com/danimalabares/archive/blob/main/archive/HOW_TO_GIVE_A_TALK.txt), saved verbatim from Daniel.

## Monday 16 November: current working deck

**lecture-24/lecture-24.tex/pdf: 14 essential slides.** This is the presentation to prepare and give. It keeps the central statements and implications so preparation can proceed from the whole argument to details.

**lecture-24/lecture-24-backup.tex/pdf:** the previous 54-slide draft, preserved unchanged. Its detailed notes are notes-backup.md. Use it only as supporting reference. Compile it from its folder with pdflatex lecture-24-backup.tex twice, or run make lecture-24-backup from this folder.

**lecture-24/lecture-24-appendix.tex/pdf:** the unchanged optional 32-slide KV continuation and technical backups. It is separate from the working presentation.

The new notes.md is a short list of essential understanding checkpoints. Further doubts do not automatically become additional slides. Lecture 23 is unchanged.
