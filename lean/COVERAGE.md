# Coverage

Statements and proofs written by Claude Code unless noted.
"Checked by Daniel" means he compared the Lean statement with HP.

| HP section | Tags formalized | Skipped, and why | Checked by Daniel |
|---|---|---|---|
| Commutative Algebra, Nakayama's lemma (05D7) | 05D8 05D9 05DA 05DB 05DC 05DE 05DF 05DG 05DJ 05DK 05DL 05DM 05DN | 05DD (Mathlib's `LocalizedModule` used, agreement with the tensor-product definition not proved); 05DH (not a formal statement) | no |

## HP statements corrected because of the formalization

Each has a dated note in the TeX next to the statement.

| Tag | What changed |
|---|---|
| 05DG | Nakayama: hypotheses "domain" and "nonzero ideal" removed, not used |
| 05DJ | Cayley-Hamilton: matrix is a choice relative to generators; conclusion is P(phi)=0, not P(A)=0 |
