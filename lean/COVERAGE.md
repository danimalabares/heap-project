# Coverage

Statements and proofs written by Claude Code unless noted.
"Checked by Daniel" means he compared the Lean statement with HP.

| HP section | Tags formalized | Skipped, and why | Checked by Daniel |
|---|---|---|---|
| Commutative Algebra, first five sections: Rings, Polynomial rings, gcd and lcm, Euclidean domains, PIDs (058N-0594) | 058P 058Q 058R 058T 058V 058X 058Z 0591 0592 0593 0594, 07Q8 in part | 058W (polynomial gcd by degree: HP itself leaves it tentative); the two exercises of Polynomial rings; the divisibility chain and nonvanishing in lemma-pid-free-module; 0593 is Mathlib's instance for Mathlib's notion of Euclidean domain | no |
| Commutative Algebra, UFDs and the Gauss lemma (0595) | 0596 0597 0598 0599 059A 059B 059C 059G 059H; 059F for polynomials over R only | 059E (Lang's order and content over the fraction field: not in Mathlib) and so 059F as stated; 059D (remark); exercise-rational-functions-irreducible | no |
| Commutative Algebra: Modules, Invariant factors theorem, Algebras, Spectrum of a ring, Localization | 059R 059T 059U 059W 059Y 059Z 07QA 07QB 07QD 08DK (some in part, see docstrings) | invariant factor form and Jordan canonical form (not in Mathlib); HP's form of finite presentation; exercise-maximal-spectrum | no |
| Commutative Algebra: Noetherian and Artinian rings, Tensor product | 05A1 05A2 05A3 05A4 05A5 05A8 05AA 05AB 05AC 05AH 05AM 05AP 05AR 05AX 08DN 08DP | Tensor product: the exercises asking for examples, Hom(N,-) left exactness, injective modules, finitely generated projective iff summand, the two lemmas on Hom and exactness, R/I tensor R/I' = 0, all statements about varieties and Spec, reducedness of tensor products over C; lemma-diagonal-of-product (its HP statement is cut off: no conclusion) | no |
| Commutative Algebra, Nakayama's lemma (05D7) | 05D8 05D9 05DA 05DB 05DC 05DE 05DF 05DG 05DJ 05DK 05DL 05DM 05DN | 05DD (Mathlib's `LocalizedModule` used, agreement with the tensor-product definition not proved); 05DH (not a formal statement) | no |

## HP statements corrected because of the formalization

Each has a dated note in the TeX next to the statement.

| Tag | What changed |
|---|---|
| 05DG | Nakayama: hypotheses "domain" and "nonzero ideal" removed, not used |
| 05DJ | Cayley-Hamilton: matrix is a choice relative to generators; conclusion is P(phi)=0, not P(A)=0 |
| 058P | Domain: the ring must be nonzero |
| 058V | gcd and lcm: the gcd must divide both, both must divide the lcm (otherwise 0 and 1 qualify) |
| 058Z, 0591 | Euclidean domain: the earlier definition was unsatisfiable (a = b = 0); now excludes division by zero and allows zero remainder |
| exercise-ring-of-plane-curve-is-pid | Counterexample is C[x,y]/(y^3-x^2), not (y-x^2); found while reading, not formalized |
| 0599 | Division algorithm for polynomials over a field: needs g nonzero |
| 059B | Second sentence now says f is irreducible |
| definition-localization | Equality of fractions needs a factor t in S when R has zero divisors |

## Next

Commutative Algebra from "Flat modules" onward, then the rest of the chapter. Left over in "Tensor product": lemma-diagonal-of-product (HP statement has no conclusion; fix and formalize), R/I tensor R/I' = 0, Hom(N,-) left exactness, finitely generated projective iff direct summand. The Noetherian and Tensor sections have no pointer to their Lean file in the TeX yet.
