# English exam: positive curvature gives coordinates

A ten-minute talk on Kodaira's embedding theorem for an English exam. The mathematics is a sketch; clear speaking matters most.

- Source: `english-exam.tex`
- Presentation: `english-exam.pdf` (generated locally, following the repository's PDF ignore rule)
- Rehearsal: `speaker-notes.md`

Build from this directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error english-exam.tex
pdflatex -interaction=nonstopmode -halt-on-error english-exam.tex
```

The deck uses `../preamble.tex` and the Kodaira photo in `../assets/`.

## Structure

1. Slides 1–13, the timed talk (about nine minutes): the Fubini–Study form is positive; Kodaira's theorem is the converse; the canonical map and its three conditions; lifting through vanishing of H^1; Hodge theory and the Bochner–Kodaira formula, which shows that harmonic forms vanish.
2. Slides 14–25, an appendix: a short history of complex and Kähler geometry from Riemann (1851) to Chen–Donaldson–Sun (2015), ending with the hyperkähler line (Beauville, Huybrechts' projectivity criterion, the SYZ conjecture). It is not part of the timed talk.

## Scope and sources

The blow-up reduction on the lifting slide is stated, not proved (Griffiths–Harris, Ch. 1 §4). The Bochner–Kodaira and Fubini–Study slides follow `../lecture-23/lecture-23.tex` and `../plan/slides.tex`.

The publication data in the appendix (Fubini 1904, Study 1905, Kähler 1933, Hodge 1941, Weyl 1943, Bochner 1946, Chow 1949, Kodaira 1953 and 1954, Serre 1956, Calabi 1954 and 1957, Yau 1977 and 1978, Voisin 2004) were checked by Claude against bibliographic records on 2026-11-04. The remaining historical statements (Hartogs, Poincaré, Lefschetz's quotation, Newlander–Nirenberg, Kodaira–Spencer, Hörmander, Chen–Donaldson–Sun) are standard but were not individually rechecked. Huybrechts' projectivity criterion and the 2003 erratum follow the HP section *Reading the masters*, Huybrechts. The SYZ statement is a conjecture.

The Kodaira photo is credited to Konrad Jacobs / MFO, CC BY-SA 2.0 Germany, https://commons.wikimedia.org/wiki/File:Kodaira_Kunihiko.jpg . His Fields Medal year follows https://www.ias.edu/scholars/kunihiko-kodaira .
