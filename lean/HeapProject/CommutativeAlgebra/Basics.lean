/-
Heap Project, Commutative Algebra, Sections "Rings" (058N),
"Polynomial rings" (058S), "Greatest common divisor and least common
multiple" (058U), "Euclidean domains" (058Y) and "Principal ideal
domains".

Each declaration carries the permanent HP tag of the statement it
formalizes (https://www.heap-project.org/tag/TAG).  Statements and
proofs were written by Claude Code from `commutative-algebra.tex`; a
proof here certifies the Lean statement, so the match between the Lean
statement and the HP statement has to be checked by a human.
-/
import Mathlib.Algebra.EuclideanDomain.Int
import Mathlib.Algebra.Polynomial.Div
import Mathlib.LinearAlgebra.FreeModule.PID
import Mathlib.NumberTheory.Zsqrtd.GaussianInt
import Mathlib.RingTheory.Ideal.Maps
import Mathlib.RingTheory.Ideal.Quotient.Operations
import Mathlib.RingTheory.Polynomial.RationalRoot
import Mathlib.RingTheory.Polynomial.UniqueFactorization
import Mathlib.RingTheory.PrincipalIdealDomain
import Mathlib.RingTheory.UniqueFactorizationDomain.GCDMonoid

namespace HeapProject.CommutativeAlgebra

open Polynomial

variable {R : Type*} [CommRing R]

/-! ### Rings -/

/-- HP tag 058P (definition-domain).  A ring is a domain if `a * b = 0`
implies `a = 0` or `b = 0`.  Mathlib's `IsDomain` also asks that the
ring is not the zero ring; HP now says so too (corrected on
24 November 2026). -/
theorem isDomain_iff :
    IsDomain R ↔
      Nontrivial R ∧ ∀ a b : R, a * b = 0 → a = 0 ∨ b = 0 := by
  constructor
  · intro h
    exact ⟨inferInstance, fun a b hab => mul_eq_zero.mp hab⟩
  · rintro ⟨_, h⟩
    haveI : NoZeroDivisors R := ⟨fun {a b} hab => h a b hab⟩
    exact NoZeroDivisors.to_isDomain R

/-- HP tag 058Q (theorem-ideal-quoti-corre), first half.  An ideal `J`
containing `I` is recovered from its image in `R / I`. -/
theorem comap_map_mk_of_le (I J : Ideal R) (h : I ≤ J) :
    (J.map (Ideal.Quotient.mk I)).comap (Ideal.Quotient.mk I) = J := by
  rw [Ideal.comap_map_of_surjective _ Ideal.Quotient.mk_surjective,
    ← RingHom.ker_eq_comap_bot, Ideal.mk_ker, sup_eq_left.2 h]

/-- HP tag 058Q (theorem-ideal-quoti-corre), second half.  An ideal of
`R / I` is the image of its preimage, and the preimage contains `I`. -/
theorem map_comap_mk (I : Ideal R) (K : Ideal (R ⧸ I)) :
    (K.comap (Ideal.Quotient.mk I)).map (Ideal.Quotient.mk I) = K ∧
      I ≤ K.comap (Ideal.Quotient.mk I) := by
  refine ⟨Ideal.map_comap_of_surjective _
    Ideal.Quotient.mk_surjective K, fun x hx => ?_⟩
  rw [Ideal.mem_comap, Ideal.Quotient.eq_zero_iff_mem.2 hx]
  exact K.zero_mem

/-- HP tag 058R (lemma-quoti-ring-maxim-ideal-field).  The quotient of
a ring by a maximal ideal is a field. -/
theorem isField_quotient_of_isMaximal (I : Ideal R) [hI : I.IsMaximal] :
    IsField (R ⧸ I) :=
  (Ideal.Quotient.maximal_ideal_iff_isField_quotient I).1 hI

/-! ### Polynomial rings -/

/-- HP tag 058T (lemma-ring-polyn-one-indet-over).  The ring of
polynomials in one indeterminate over a domain is a domain. -/
theorem isDomain_polynomial [IsDomain R] : IsDomain R[X] :=
  inferInstance

/-! ### Greatest common divisor and least common multiple -/

section GCD

variable {α : Type*} [CommMonoidWithZero α]

/-- HP tag 058V (definition-lcm-and-gdc-universal), gcd.  `d` is a
greatest common divisor of `a` and `b` if it divides both and every
common divisor divides it.

HP did not ask that `d` divides `a` and `b`; without that, `0` is a
gcd of any two elements.  Corrected in HP on 24 November 2026. -/
def IsGCD (a b d : α) : Prop :=
  d ∣ a ∧ d ∣ b ∧ ∀ c, c ∣ a → c ∣ b → c ∣ d

/-- HP tag 058V (definition-lcm-and-gdc-universal), lcm.  `l` is a
least common multiple of `a` and `b` if both divide it and it divides
every common multiple.

HP did not ask that `a` and `b` divide `l`; without that, `1` is an
lcm of any two elements.  Corrected in HP on 24 November 2026. -/
def IsLCM (a b l : α) : Prop :=
  a ∣ l ∧ b ∣ l ∧ ∀ c, a ∣ c → b ∣ c → l ∣ c

/-- The reason for the correction of HP tag 058V: with the earlier
wording, `0` satisfies the gcd condition for any `a` and `b`. -/
theorem zero_satisfies_earlier_gcd (a b : α) :
    ∀ c, c ∣ a → c ∣ b → c ∣ (0 : α) :=
  fun c _ _ => dvd_zero c

/-- The reason for the correction of HP tag 058V: with the earlier
wording, `1` satisfies the lcm condition for any `a` and `b`. -/
theorem one_satisfies_earlier_lcm (a b : α) :
    ∀ c, a ∣ c → b ∣ c → (1 : α) ∣ c :=
  fun c _ _ => one_dvd c

/-- Part of HP tag 058X: a gcd is unique up to multiplication by a
unit. -/
theorem IsGCD.associated [IsCancelMulZero α] {a b d d' : α}
    (h : IsGCD a b d) (h' : IsGCD a b d') : Associated d d' :=
  associated_of_dvd_dvd (h'.2.2 d h.1 h.2.1) (h.2.2 d' h'.1 h'.2.1)

/-- Part of HP tag 058X: an lcm is unique up to multiplication by a
unit. -/
theorem IsLCM.associated [IsCancelMulZero α] {a b l l' : α}
    (h : IsLCM a b l) (h' : IsLCM a b l') : Associated l l' :=
  associated_of_dvd_dvd (h.2.2 l' h'.1 h'.2.1) (h'.2.2 l h.1 h.2.1)

end GCD

/-- HP tag 058X (lemma-existence-of-lcm-and-gcd).  If `R` is a UFD then
any two polynomials in `R[x]` have a gcd and an lcm.  Uniqueness up to
units is `IsGCD.associated` and `IsLCM.associated`. -/
theorem exists_isGCD_and_isLCM_polynomial [IsDomain R]
    [UniqueFactorizationMonoid R] (f g : R[X]) :
    (∃ d, IsGCD f g d) ∧ (∃ l, IsLCM f g l) := by
  obtain ⟨_⟩ := (inferInstance : Nonempty (NormalizedGCDMonoid R[X]))
  exact ⟨⟨gcd f g, gcd_dvd_left f g, gcd_dvd_right f g,
      fun c => dvd_gcd⟩,
    ⟨lcm f g, dvd_lcm_left f g, dvd_lcm_right f g,
      fun c => lcm_dvd⟩⟩

/-! ### Euclidean domains -/

/-- HP tag 058Z (definition-euclidean-domain).  A Euclidean function
on `R`: `φ a ≤ φ (a * b)` for nonzero `a`, `b`, and division with
remainder by any nonzero `b`.  A domain is Euclidean if it has one.

HP's earlier wording could not be satisfied by any ring (see
`not_earlier_euclidean`); it was corrected on 24 November 2026.  The
values of `φ` are taken in `ℕ`; the value at `0` plays no role. -/
structure IsEuclideanFunction (φ : R → ℕ) : Prop where
  le_mul : ∀ a b : R, a ≠ 0 → b ≠ 0 → φ a ≤ φ (a * b)
  div : ∀ a b : R, b ≠ 0 →
    ∃ q r : R, a = b * q + r ∧ (r = 0 ∨ φ r < φ b)

/-- The reason for the correction of HP tag 058Z: the earlier second
condition (for all `a`, `b` with `φ a ≥ φ b` there are `q`, `r` with
`a = b q + r` and `φ r < φ b`) fails for `a = b = 0`, for every `φ`. -/
theorem not_earlier_euclidean (φ : R → ℕ) :
    ¬ ∀ a b : R, φ b ≤ φ a →
      ∃ q r : R, a = b * q + r ∧ φ r < φ b := by
  intro h
  obtain ⟨q, r, hr, hlt⟩ := h 0 0 le_rfl
  have hr0 : r = 0 := by simpa using hr.symm
  rw [hr0] at hlt
  exact lt_irrefl _ hlt

/-- HP tag 0591 (remark-equivalence-for-valuation).  The first
condition of a Euclidean function is equivalent to: if `a` divides a
nonzero `b` then `φ a ≤ φ b`. -/
theorem le_mul_iff_le_of_dvd [IsDomain R] (φ : R → ℕ) :
    (∀ a b : R, a ≠ 0 → b ≠ 0 → φ a ≤ φ (a * b)) ↔
      ∀ a b : R, b ≠ 0 → a ∣ b → φ a ≤ φ b := by
  constructor
  · rintro h a b hb ⟨c, rfl⟩
    exact h a c (left_ne_zero_of_mul hb) (right_ne_zero_of_mul hb)
  · intro h a b ha hb
    exact h a (a * b) (mul_ne_zero ha hb) (dvd_mul_right a b)

/-- The integers are Euclidean in the sense of HP tag 058Z, with the
absolute value (mentioned after HP tag 0593). -/
theorem isEuclideanFunction_natAbs : IsEuclideanFunction Int.natAbs where
  le_mul a b _ hb := by
    rw [Int.natAbs_mul]
    exact Nat.le_mul_of_pos_right _ (Int.natAbs_pos.2 hb)
  div a b hb := by
    refine ⟨a / b, a % b, (Int.mul_ediv_add_emod a b).symm, Or.inr ?_⟩
    rw [← Int.ofNat_lt, Int.natCast_natAbs, Int.natCast_natAbs,
      abs_of_nonneg (Int.emod_nonneg a hb)]
    exact Int.emod_lt_abs a hb

/-- HP tag 0592 (theorem-eucli-algor-polyn-rings).  If the leading
coefficient of `g` is a unit then any `f` can be divided by `g` with
a remainder of smaller degree.

HP assumes that `R` is a domain and that `deg f ≥ deg g`; here `R` is
any nonzero ring and there is no condition on the degree of `f`. -/
theorem exists_div_rem_of_isUnit_leadingCoeff [Nontrivial R]
    (f g : R[X]) (hg : IsUnit g.leadingCoeff) :
    ∃ q r : R[X], f = q * g + r ∧ r.degree < g.degree := by
  have hm : (hg.unit⁻¹ • g).Monic :=
    Polynomial.monic_of_isUnit_leadingCoeff_inv_smul hg
  have hdeg : (hg.unit⁻¹ • g).degree = g.degree :=
    Polynomial.degree_smul_of_smul_regular g (isSMulRegular_of_group _)
  refine ⟨hg.unit⁻¹ • (f /ₘ (hg.unit⁻¹ • g)), f %ₘ (hg.unit⁻¹ • g),
    ?_, ?_⟩
  · conv_lhs => rw [← Polynomial.modByMonic_add_div f (hg.unit⁻¹ • g)]
    rw [smul_mul_assoc, smul_mul_assoc, add_comm, mul_comm]
  · rw [← hdeg]
    exact Polynomial.degree_modByMonic_lt f hm

/-- HP tag 0593 (exercise-gaussian-integers-euclidean).  The ring of
Gaussian integers is Euclidean.  This is Mathlib's instance, for
Mathlib's notion of Euclidean domain (a well-founded relation instead
of a function to `ℕ`), not for `IsEuclideanFunction`. -/
noncomputable example : EuclideanDomain GaussianInt := inferInstance

/-- HP tag 0594 (lemma-euclidan-is-ufd).  A PID is integrally
closed. -/
theorem isIntegrallyClosed_of_pid [IsDomain R] [IsPrincipalIdealRing R] :
    IsIntegrallyClosed R :=
  inferInstance

/-! ### Principal ideal domains -/

open Module in
/-- HP tag 07Q8 (lemma-pid-free-module), in part.  Let `R` be a PID, `M` a free
module of finite rank and `N` a submodule.  Then `N` is free of rank
`m ≤ n`, and there are a basis `y` of `M` and elements `a i` such that
the `a i • y i` for `i < m` form a basis of `N`.

Not formalized: that the `a i` are nonzero and that each divides the
next.  The basis `y` is given as a basis of the top submodule of `M`,
which is `M` itself. -/
theorem exists_smith_basis [IsDomain R] [IsPrincipalIdealRing R]
    {M : Type*} [AddCommGroup M] [Module R M] {ι : Type*} [Finite ι]
    (b : Basis ι R M) (N : Submodule R M) :
    ∃ (m n : ℕ) (hmn : m ≤ n)
      (y : Basis (Fin n) R (⊤ : Submodule R M))
      (bN : Basis (Fin m) R N) (a : Fin m → R),
      ∀ i, (bN i : M) = a i • (y (Fin.castLE hmn i) : M) :=
  Submodule.exists_smith_normal_form_of_le b N ⊤ le_top

end HeapProject.CommutativeAlgebra
