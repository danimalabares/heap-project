# Kodaira lectures


| Folder | Draft | Slides |
| --- | --- | ---: |
| [lecture-23](lecture-23/lecture-23.tex) | Embedding mechanism and Nadel vanishing | 61 |
| [lecture-24](lecture-24/lecture-24.tex) | Essential embedding proof | 14 working; 32 optional |

These two decks form one continuous argument, with a short course recap and Kodaira embedding as the initial goal. The first lecture explains how H1-vanishing gives values and first jets before developing Nadel. They retain the dbar-poincare Beamer style, use mathematical pictures and short historical pauses, and move longer technical arguments into optional preparation notes. Shared styling is in [preamble.tex](preamble.tex).

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

For lecture 24, use folder `lecture-24` and source `lecture-24.tex`. The lecture outputs are `lecture-23/lecture-23.pdf` and `lecture-24/lecture-24.pdf`. Compiled PDFs remain local, following the repository's existing PDF ignore rule.

## Mathematical scope

Lecture 23 opens with two recap slides covering the course from complex structures to singular psh weights. It then states Kodaira embedding, explains why point and tangent separation suffice, and proves the mechanism from the evaluation exact sequence. This motivates the multiplier ideal, the weighted Dolbeault resolution, and the Nadel deduction. Bochner–Kodaira and Kodaira vanishing are brief reminders. The weighted local lemma and singular-weight L2 existence theorem remain explicit analytic inputs. Hahn–Banach, operator domains, and approximation details are optional notes.

Lecture 24 is now an essentials-only working presentation: the vanishing and its analytic mechanism, the global singular metric, values and first jets, embedding, and Chow. The separate optional KV appendix is unchanged.

## Monday 16 November: current working deck

**lecture-24/lecture-24.tex/pdf: 14 essential slides.** This is the presentation to prepare and give. It keeps the central statements and implications so preparation can proceed from the whole argument to details.

**lecture-24/lecture-24-appendix.tex/pdf:** the unchanged optional 32-slide KV continuation and technical backups. It is separate from the working presentation.
