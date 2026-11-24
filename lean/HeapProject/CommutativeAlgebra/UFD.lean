/-
Heap Project, Commutative Algebra, Section "Unique factorization
domains and the Gauss lemma" (0595).

Each declaration carries the permanent HP tag of the statement it
formalizes (https://www.heap-project.org/tag/TAG).  Statements and
proofs were written by Claude Code from `commutative-algebra.tex`; a
proof here certifies the Lean statement, so the match between the Lean
statement and the HP statement has to be checked by a human.
-/
import Mathlib.Algebra.Polynomial.FieldDivision
import Mathlib.Data.Int.GCD
import Mathlib.RingTheory.Ideal.Maximal
import Mathlib.RingTheory.Polynomial.Content
import Mathlib.RingTheory.Polynomial.UniqueFactorization
import Mathlib.RingTheory.PrincipalIdealDomain
import Mathlib.RingTheory.UniqueFactorizationDomain.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring

namespace HeapProject.CommutativeAlgebra

open Polynomial

variable {R : Type*} [CommRing R]
variable {F : Type*} [Field F]

/-- HP tag 0596 (lemma-irreducible-is-prime).  In a UFD, irreducible
elements are prime. -/
theorem prime_of_irreducible_of_ufd [UniqueFactorizationMonoid R]
    {p : R} (hp : Irreducible p) : Prime p :=
  UniqueFactorizationMonoid.irreducible_iff_prime.1 hp

/-- HP tag 0597 (theorem-Bachet-Bezout-for-integers).  For integers
`a`, `b` there are `x`, `y` with `a x + b y = gcd(a, b)`; hence a
common divisor of `a` and `b` divides `gcd(a, b)`. -/
theorem int_bezout (a b : ℤ) :
    (∃ x y : ℤ, a * x + b * y = Int.gcd a b) ∧
      ∀ c : ℤ, c ∣ a → c ∣ b → c ∣ (Int.gcd a b : ℤ) :=
  ⟨⟨Int.gcdA a b, Int.gcdB a b, (Int.gcd_eq_gcd_ab a b).symm⟩,
    fun _ ha hb => Int.dvd_coe_gcd ha hb⟩

/-- HP tag 0598 (lemma-relat-prime-divid-impli-divid).  If `a` divides
`b c` and `gcd(a, b) = 1` then `a` divides `c`. -/
theorem int_dvd_of_dvd_mul_of_gcd_eq_one {a b c : ℤ} (h : a ∣ b * c)
    (hab : Int.gcd a b = 1) : a ∣ c :=
  Int.dvd_of_dvd_mul_right_of_gcd_one h hab

/-- Uniqueness in HP tag 0599: quotient and remainder of a division
with remainder of smaller degree are unique. -/
theorem div_rem_unique {g q q' r r' : F[X]}
    (h : q * g + r = q' * g + r')
    (hr : r.degree < g.degree) (hr' : r'.degree < g.degree) :
    q = q' ∧ r = r' := by
  have hq : q = q' := by
    by_contra hne
    have h1 : (q - q') * g = r' - r := by linear_combination h
    have h0 : (0 : WithBot ℕ) ≤ (q - q').degree :=
      Polynomial.zero_le_degree_iff.2 (sub_ne_zero.2 hne)
    have h2 : g.degree ≤ ((q - q') * g).degree := by
      rw [Polynomial.degree_mul]
      exact le_add_of_nonneg_left h0
    have h3 : (r' - r).degree < g.degree :=
      lt_of_le_of_lt (Polynomial.degree_sub_le _ _) (max_lt hr' hr)
    rw [h1] at h2
    exact absurd h3 (not_lt.2 h2)
  refine ⟨hq, ?_⟩
  subst hq
  exact add_left_cancel h

/-- HP tag 0599 (theorem-divis-algor-polyn).  Over a field, for `f` and
a nonzero `g` there are unique `q`, `r` with `f = q g + r` and
`deg r < deg g`.

HP did not ask `g ≠ 0`; for `g = 0` no `r` has smaller degree.
Corrected in HP on 24 November 2026. -/
theorem existsUnique_div_rem (f g : F[X]) (hg : g ≠ 0) :
    ∃! p : F[X] × F[X], f = p.1 * g + p.2 ∧ p.2.degree < g.degree := by
  refine ⟨(f / g, f % g), ⟨?_, Polynomial.degree_mod_lt f hg⟩, ?_⟩
  · rw [mul_comm]
    exact (EuclideanDomain.div_add_mod f g).symm
  · rintro ⟨q, r⟩ ⟨h1, h2⟩
    have h : q * g + r = f / g * g + f % g := by
      rw [← h1, mul_comm (f / g) g]
      exact (EuclideanDomain.div_add_mod f g).symm
    obtain ⟨hq, hr⟩ :=
      div_rem_unique h h2 (Polynomial.degree_mod_lt f hg)
    exact Prod.ext hq hr

/-- The reason for the correction of HP tag 0599: nothing has degree
smaller than that of the zero polynomial. -/
theorem not_degree_lt_degree_zero (r : F[X]) :
    ¬ r.degree < (0 : F[X]).degree := by
  simp

open scoped Classical in
/-- HP tag 059A (theorem-bache-bezou-polyn-over-fiel).  Over a field,
for polynomials `f`, `g` there are `p`, `q` with
`f p + g q = gcd(f, g)`. -/
theorem polynomial_bezout (f g : F[X]) :
    ∃ p q : F[X], f * p + g * q = EuclideanDomain.gcd f g :=
  ⟨EuclideanDomain.gcdA f g, EuclideanDomain.gcdB f g,
    (EuclideanDomain.gcd_eq_gcd_ab f g).symm⟩

/-- HP tag 059B (lemma-irreducible-is-prime-in-F[x]).  Over a field,
if an irreducible polynomial `f` divides `g h` then it divides `g` or
`h`. -/
theorem polynomial_dvd_or_dvd_of_irreducible {f g h : F[X]}
    (hf : Irreducible f) (hd : f ∣ g * h) : f ∣ g ∨ f ∣ h :=
  hf.prime.dvd_or_dvd hd

/-- HP tag 059C (lemma-polynomials-over-fields-are-UFD).  The
polynomial ring over a field is a UFD. -/
theorem ufd_polynomial_field : UniqueFactorizationMonoid F[X] :=
  inferInstance

/-- HP tag 059F (lemma-true-Gauss), for polynomials with coefficients
in `R`: the content of a product is the product of the contents.

HP states this for polynomials over the fraction field of `R`, with
Lang's content (HP tag 059E), which Mathlib does not have.  This is
the statement for Mathlib's content of polynomials over `R`, the gcd
of the coefficients. -/
theorem content_mul_of_ufd [NormalizedGCDMonoid R] (f g : R[X]) :
    (f * g).content = f.content * g.content :=
  Polynomial.content_mul

/-- HP tag 059G (lemma-R-UFD-implies-R[x]-UFD; Gauss).  If `R` is a
UFD then `R[x]` is a UFD. -/
theorem ufd_polynomial_of_ufd [UniqueFactorizationMonoid R] :
    UniqueFactorizationMonoid R[X] :=
  inferInstance

/-- HP tag 059H (lemma-ufd-irred-eleme-gener-prime).  In a UFD,
irreducible elements generate prime ideals. -/
theorem span_singleton_isPrime_of_irreducible
    [UniqueFactorizationMonoid R] {p : R} (hp : Irreducible p) :
    (Ideal.span {p}).IsPrime :=
  (Ideal.span_singleton_prime hp.ne_zero).2
    (UniqueFactorizationMonoid.irreducible_iff_prime.1 hp)

end HeapProject.CommutativeAlgebra
