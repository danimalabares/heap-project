# Hodge theory: Lectures 12 and 13

Plain black-and-white Beamer slides, in 16:9 format.

- [Lecture 12 source](lecture-12/lecture-12.tex): Fourier modes on the torus, complex
  Cartan, and the one-variable dbar-Poincare lemma.
- [Lecture 13 source](lecture-13/lecture-13.tex): the Dolbeault resolution, the
  several-variable local lemma, and Hartogs extension.

## Lecture 13

The opening explains sections and stalks, image sheaves and sheafification,
fine sheaves, injective resolutions, and Voisin's Proposition 4.32.
A degree-one long exact sequence explains how the proposition works.

The remaining slides follow Misha's Lecture 13:

1. Recall the Fourier homotopy on an elliptic curve.
2. Construct a linear solution operator on a disk and explain its
   dependence on parameters.
3. Define the coordinate homotopies and the spaces `R_i` and `W_k`.
   Prove the local lemma using Misha's filtration, with a two-variable example.
4. Prove Hartogs extension by solving the compactly supported error form
   on projective space, using Hodge theory and Liouville's theorem.

The homotopy argument uses nested polydisks inside the domain where the
input form is smooth and closed. The slides distinguish this local result
from the stronger theorem on an entire open polydisk without a boundary
extension assumption.

Hartogs' theorem includes the connected-complement hypothesis. Its proof
explains both the vanishing of `H^{0,1}(P^n)` and why the correcting
function is constant outside a ball.

## Build

HP builds the decks with `make gerby-slides`; to build one by hand, run
`pdflatex` twice in its folder (see `../README.md`).

## Sources and conventions

- Misha Verbitsky, Hodge theory, IMPA 2025:
  [Lecture 12](http://verbit.ru/IMPA/Kahler-2025/slides-Kahler-2025-12.pdf)
  and [Lecture 13](http://verbit.ru/IMPA/Kahler-2025/slides-Kahler-2025-13.pdf).
- [Heap Project](https://github.com/danimalabares/heap-project):
  complex geometry, complex analysis, and Hodge theory.
- Claire Voisin, *Hodge Theory and Complex Algebraic Geometry I*,
  Chapter 4, especially Propositions 4.32 and 4.36.
  The numbering follows the
  [de Rham and Dolbeault notes](../../archive/de-rham-dolbeault/de-rham-dolbeault.tex).
- Daniel Huybrechts, *Complex Geometry: An Introduction*,
  Propositions 1.3.7-1.3.8 and Corollary 1.3.9.

We use `z=x+iy`, `partial_bar_z=(partial_x+i partial_y)/2`,
and `dbar f=partial_bar_z(f) dbar z`.
With `I(partial_x)=partial_y`, complex Cartan's formula for dbar uses
`(L_X+i L_IX)/2`. The Fourier multiplier is therefore `(in-m)/2`.

Portraits appear on separate slides.
