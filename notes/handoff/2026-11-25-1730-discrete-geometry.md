# Handoff: Part III Combinatorics and Discrete Geometry; SR chapter cleanup

Date: 2026-11-25, about 17:30 (Claude Code, Fable 5.2).
Worktree: `~/github/heap-discrete-geometry`, branch `feat/discrete-geometry`
(from origin/main at bfa13631a). Nothing is pushed or merged.
`notes/status.md` was not edited (other sessions hold it).

## What Daniel asked (his words, shortened)

1. "Check out the proof that a smoothing of a triangulation of a sphere is a
   CY in [slides, live.html#12]. Let's write this proof on the Heap, in the
   SR chapter, which btw probably needs to be cleaned up. Decide if some
   parts of this chapter should be somewhere else. Recall that the Heap is
   not a research notebook: it's a general knowledge notebook, so the
   grunbaum sphere probably should not be discussed with so much detail."
2. "A new Heap part for Combinatorics, or perhaps discrete geometry. Here we
   can put the Combinatorics chapter which now is in algebra, and all the
   stuff on polytopality, and, finally, skeletal polytopes. For skeletal
   polytopes the main definitions shall come from my masters thesis, put
   that text verbatim and cite the thesis. Also we should include the
   material described in my bachelor's thesis, including pictures, which
   should be available in my Drive. Watch out: another agent(s?) is also
   doing lots of stuff in the Heap."

## Done on this branch

- New Part III "Combinatorics and Discrete Geometry" in `order-chapters.txt`:
  Combinatorics (moved from Part II), Tessellations of the plane, Polytopes,
  Skeletal polytopes. Later Parts renumbered (Seminars XII, Conferences
  XIII, Minicourses XIV; AGENTS.md updated).
- Three chapters registered with the heap-project-chapter script:
  `plane-tessellations.tex` (code `te`, still EMPTY), `polytopes.tex`
  (`po`), `skeletal-polytopes.tex` (`ks`; `sk` was taken).
  `~/github/config/aliases.sh` has the alias blocks, UNCOMMITTED.
- `skeletal-polytopes.tex`: sections 2 to 6 of the tesina verbatim
  (source `standalone/sources/chiral-4-polytope/tesina.tex`), macros
  expanded, cited as `gca-tesina`. Compiles clean.
- `polytopes.tex`: short introduction, the Holleben-Yang polytopality
  sections and the 6-vertex RP2 section moved from the SR chapter
  (subsections became sections, labels kept), a short section on the
  Grünbaum-Sreedharan sphere.
- `stanley-reisner.tex` now has: definitions; the dualizing sheaf of a
  sphere, ending with Theorem `theorem-fausk-021` (a smooth fibre near the
  SR scheme of a d-sphere is K3 / Calabi-Yau) with a four-step proof; the
  Grünbaum-Sreedharan sphere (ideal only); the three CP2_9 / Calla sections.
- Moved out of the SR chapter: Misha's dual-complex seminar to
  `seminars-complex-geometry.tex`; "Dual complex of a degeneration" (KLSV)
  and "Degenerations of Hilbert schemes" to `hilbert-schemes.tex`; the
  "GN variety" research diary to the research repo,
  `~/github/daniel-grunbaum/grunbaum/archive/hp-gn-variety-notes.tex`.
- 27 label migrations added to `scripts/gerby_label_migrations.json`.
- The section "The dualizing sheaf" in `algebraic-geometry.tex` and the
  first version of the SR section were written by the slides session
  (f4164717) and sit UNCOMMITTED in the main checkout `~/github/heap-project`
  (algebraic-geometry.tex, stanley-reisner.tex, my.bib). I copied that diff
  here and edited on top of it.

## Sources checked (read in text extracted with gs, in ~/books)

- Hartshorne III 6.5, 7.2, 7.5, 7.7, 7.11, 7.12, 12.8, 12.11, II 8.20.1:
  numbers and statements correct. Step 2 of the proposition now names
  12.11 (a) and (b).
- Stanley, Combinatorics and Commutative Algebra, 2nd ed.: II Cor 4.2
  (Reisner), II Thm 4.8 (Hochster), II Thm 5.1 and Cor 5.2, I Thm 12.5 and
  12.6, II Section 7.
- Bayer-Eisenbud, Graph curves: Theorem 6.1 (canonical bundle of the face
  variety of a compact manifold is trivial iff orientable) and the
  unnumbered statement H^i(X,O_X) = reduced cohomology of M for i>0.
- Stacks Project (local checkout): Tags 0BFQ, 0C09, 0E2Y, 0E2Z.
- NOT checked: Fausk Theorem 0.2.1 (no copy); how the families fact before
  `proposition-trivial-dualizing-nearby` follows from the Stacks tags; the
  residue description of the dualizing sheaf of a nodal curve.

## Still to do

1. `plane-tessellations.tex`: the bachelor's thesis ("Las simetrías de las
   teselaciones en el plano", UNAM 2021, bib key `gca-tesis-licenciatura`).
   PDF: `~/archive/coursework/tesis-licenciatura/TesisDaniel.pdf` (same file
   as `standalone/simetrias-teselaciones-plano.pdf`); no TeX source.
   Text: `gs -q -dNOPAUSE -dBATCH -sDEVICE=txtwrite -sOutputFile=out.txt`.
   Pictures: `~/archive/coursework/tesis-licenciatura/Figuras/*.jpeg`, or
   render pages with gs (`-sDEVICE=png16m`). Put them in
   `plane-tessellations-assets/` and add `!plane-tessellations-assets/*`
   lines to `.gitignore`, as for `algebraic-topology-assets`. No poppler on
   this Mac; the Read tool cannot open PDFs.
2. `make gerby-register` (allocates tags; do it after rebasing on the
   current origin/main, since other sessions also allocate), then
   `make gerby-book`, registry check, and the route tests.
3. Rebase or merge with origin/main: other sessions have uncommitted edits
   to Makefile, order-chapters.txt, preamble.tex, make_gerby_book.py in the
   main checkout (new chapters philosophy, topological-groups,
   birman-hilden). Expect conflicts there.
4. Before merging, the main checkout's uncommitted copies of
   algebraic-geometry.tex, stanley-reisner.tex and my.bib must be dealt
   with: this branch supersedes them. Ask Daniel; do not discard another
   session's files without his word.
5. Commit and push `~/github/config/aliases.sh` once the chapters are on
   main. Update shared memory (config/memory) with the new Part.
6. The research-kit hook refuses Write of a .tex with `\bibliographystyle`
   and in-place latexmk. HP uses classic BibTeX and `make NAME.pdf` on
   purpose; either add `.claude/research-kit.json` with
   `"bibliography": "bibtex"` (Daniel's decision) or keep using Edit on the
   scaffold and `make`.
7. Undefined cross-chapter references in a fresh worktree go away on the
   second `make` once all `.aux` exist; `KuhnelBanchoff1983` was missing
   from my.bib and is now added.
