# Combinatorics integration — 2026-10-29

ChatGPT/Codex integrated Daniel's uploaded `combi.tex` and `PIE.png`
into `combinatorics.tex`, in Part II of HP. Daniel authorized the
integration in the Heap Project conversation on 2026-10-29.

`combi.tex.txt` is the byte-for-byte original, including its preamble,
comments, unfinished attempts and TikZ sources. The `.txt` suffix keeps
it out of chapter discovery and source-wide TeX cleanup. The source
names https://github.com/danimalabares/combi; that repository was not
used as a verified remote source. The instructor and course date remain
unknown. Spanish is retained.

## Scope and preservation

- All substantive chapters, worked examples and exercises are retained.
  Empty final exercise heading and empty umbrella headings are omitted.
- The hidden ODE detour and commented-out failed attempts remain in the
  original archive; they were not active parts of the original document.
- Five original TikZ diagrams were rendered with pdflatex and pdftoppm
  to PNG assets. The uploaded PIE image is unchanged.
- HP environments, labels, display conventions and 45-character source
  wrapping replace the standalone book preamble. No new TeX macros.
- Hall's theorem and the Stirling formula each have one statement/proof;
  other occurrences link to it. The repeated even-v Bruck--Ryser--Chowla
  condition is a reference remark. The duplicate generating-function
  definition is replaced by a reference to its definitive section.
- Probability and Stanley--Reisner connections use existing permanent
  tags 088U and 091P. No unrelated mathematical chapters were rewritten.

## Corrections made

These are targeted corrections, not a certification of the whole course.

- Multiset multiplicity sum: restore x_i. Committee/chair identity:
  restore the factor k. Negative-binomial coefficients: n-1, not n.
- Recurrences: clarify linearity, fix initial-index and missing-term
  typos, require c_k nonzero in the characteristic-root formula.
- Worked a_n=a_(n-1)+n: derivative sign and coefficient shift corrected;
  solution is 1+binomial(n+1,2).
- Derangements: D_(n-k), not D_(n-1). Inclusion-exclusion starts at A_1;
  distinguish union size from f(emptyset); state the empty-intersection
  convention. Burnside assumes finite X and uses multiplicative cosets.
- Replace informal cycle-index placeholder with its actual sum/product.
- Exercise W 1.1.2: count all rectangles, not just grid cells.
- W 1.1.3: choose consonant positions, then letters; account for repeats.
- W 1.1.8: count six-card hands by suit multiplicities (3,1,1,1) and
  (2,2,1,1), without order or repeated counting.
- W 1.1.9: state the no-leading-zero convention. The answer is 91954;
  with five positions and leading zeros allowed it is 91440. Include
  the multiplicity-partition argument so this is not merely a count.
- W 2.2.14: replace the explicitly failed generating-function attempt
  with solutions (n-1)2^n+2-n and (-7-2n)2^n+5*3^n+n+3, respectively.
- Alternating-binomial exercise: odd n rather than odd k. Mark its
  missing proof and the missing diagonal-identity proof explicitly.
- Repeated-letter exercise: state that the remaining letters differ.
- Poset isomorphisms and embeddings reflect order as well as preserve
  it; uniqueness of the representing poset is up to isomorphism.
  Finite hypotheses and inconsistent variable names are corrected.
- Hall/Dilworth: restore missing cardinality bars; SDR tuple ends in
  x_n. Hall's marriage interpretation uses union, not intersection.
  Lower bound denominator is (r-n)!, and the corollary says 'at least'.
- Sperner: restore cardinality bars. De Bruijn--Erdős: replace the false
  pairwise-line-intersection hypothesis with the finite-linear-space
  hypotheses; remove the singleton option from the near-pencil case.
- Designs: explain the 2-design convention and Fisher hypotheses;
  supply the rank/eigenvalue argument where the original asked 'why?'.
- Hadamard: absolute determinant, identity matrix notation, and correct
  3-design parameter n/4-1. Require n divisible by four in the equivalence.
- Projective planes: clarify general position and the projection inverse;
  restore q lines through each point in the line count; require q>=2.
  The missing equal-degree proof and the missing (P0) argument remain
  explicitly pending, rather than being silently treated as complete.
- Steiner systems: remove the unsupported 'largest/smallest k' claim,
  normalize congruence notation and the divisibility argument.

## References and remaining work

The original West/Cameron/Matoušek/Proofs from the Book attributions
are preserved but editions and exercise numbers have not been checked.
In particular the last three Cameron exercises repeat the same number.
The existing `generatingfunctionology` BibTeX entry is reused; this does
not certify every page number quoted in the original notes.

The corrected de Bruijn--Erdős statement was checked against §1,
pp. 49–50, of Erdős–Mullin–Sós–Stinson, *Finite linear spaces and
projective planes*, Discrete Mathematics 47 (1983), 49–62:
https://users.renyi.hu/~p_erdos/1983-05.pdf
A bibliographic entry and in-text citation were added.

The Hadamard 3-design parameter was cross-checked against Sage's
`Hadamard3Design` documentation (this is a parameter check, not a proof
of the equivalence):
https://sporadic.stanford.edu/reference/combinat/sage/combinat/designs/block_design.html

Still pending: verify the remaining named theorems against their
published references and complete the explicitly unfinished proofs.
Generalized Erdős–Ko–Rado, Bruck–Ryser–Chowla and the design equivalences
were retained from the course; a full theorem-by-theorem audit was not
performed. This distinction is also stated in the chapter introduction.

## Validation

- pdflatex/BibTeX build; PDF pages visually inspected.
- Isolated Gerby chapter render; all six PNGs present and decodable.
- Internal references resolve to permanent tag routes; original wrapped
  URL retained correctly after TeX comment-newline normalization.
- Recurrence formulas checked by substitution for n=2,...,30 and both
  initial conditions. These checks supplement the solution derivation.
- Digit answer checked by exhaustive enumeration of 0,...,99999;
  card-hand answer checked independently by inclusion-exclusion.
- All previous permanent tags preserved; new tags belong only to this
  chapter. No historical tag or snapshot was edited.
- Existing forbidden align* environments elsewhere in HP were found by
  the required repository scan and left untouched.

The local Gerby environment required a runtime-only correction to an
old plasTeX tokenizer's EndInput handling on Python 3.12 and the pdftoppm
imager. These environment changes are not repository changes. The full
site deployment is not implied by the isolated render check.

## Concurrent work

Before pushing, origin/main advanced with another agent's seminar notes
and 17 tag allocations. The source changes were reapplied in a clean
worktree based on that commit and tags were allocated anew by the
registry tool. The unpushed first allocation remains only in the local
checkpoint branch; it was not merged into the published registry.
The final chapter tag is 0GB2. All assignments from the newer remote
commit are preserved.

The config alias and shared-memory update were blocked by automatic
approval review, which considered the separate private repository
outside this request's scope. No config update is claimed here.
