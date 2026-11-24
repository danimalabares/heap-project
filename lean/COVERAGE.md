# Coverage

Statements and proofs written by Claude Code unless noted.
"Checked by Daniel" means he compared the Lean statement with HP.

| HP section | Tags formalized | Skipped, and why | Checked by Daniel |
|---|---|---|---|
| Commutative Algebra, first five sections: Rings, Polynomial rings, gcd and lcm, Euclidean domains, PIDs (058N-0594) | 058P 058Q 058R 058T 058V 058X 058Z 0591 0592 0593 0594, 07Q8 in part | 058W (polynomial gcd by degree: HP itself leaves it tentative); the two exercises of Polynomial rings; the divisibility chain and nonvanishing in lemma-pid-free-module; 0593 is Mathlib's instance for Mathlib's notion of Euclidean domain | no |
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
