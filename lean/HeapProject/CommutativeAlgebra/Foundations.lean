/-
Heap Project, Commutative Algebra, Sections "Modules", "Invariant
factors theorem", "Algebras", "Spectrum of a ring" and "Localization".

Each declaration carries the permanent HP tag of the statement it
formalizes (https://www.heap-project.org/tag/TAG).  Statements and
proofs were written by Claude Code from `commutative-algebra.tex`; a
proof here certifies the Lean statement, so the match between the Lean
statement and the HP statement has to be checked by a human.
-/
import Mathlib.Algebra.Module.PID
import Mathlib.RingTheory.FinitePresentation
import Mathlib.RingTheory.FiniteType
import Mathlib.RingTheory.Localization.Away.Basic
import Mathlib.RingTheory.Localization.Submodule
import Mathlib.RingTheory.Spectrum.Prime.Topology
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring

namespace HeapProject.CommutativeAlgebra

universe u v

variable {R : Type u} [CommRing R]

/-! ### Modules -/

/-- HP tag 059R (definition-module).  An `R`-module is an abelian group `M`
with a ring morphism `R → End(M)`: such a morphism gives a module
structure. -/
@[reducible] def moduleOfRingHom {M : Type v} [AddCommGroup M]
    (f : R →+* AddMonoid.End M) : Module R M :=
  Module.compHom M f

/-- HP tag 059R (definition-module), converse: a module structure gives a
ring morphism `R → End(M)`. -/
def ringHomOfModule (M : Type v) [AddCommGroup M] [Module R M] :
    R →+* AddMonoid.End M :=
  Module.toAddMonoidEnd R M

/-! ### Invariant factors theorem -/

open DirectSum in
/-- HP tag 07QA (exercise-invariant-factors-theorem), first sentence.  A
finitely generated module over a principal ideal domain is a direct
sum of cyclic modules: a free module and quotients `R / (p ^ e)` with
`p` irreducible.

Not formalized: the invariant factor form with `a₁ ∣ a₂ ∣ ⋯`
(HP tag 07QB (theorem-invariant-factors)) and the Jordan canonical form
(HP tag 07QD (theorem-jordan-form)); Mathlib has neither. -/
theorem exists_equiv_free_prod_directSum [IsDomain R]
    [IsPrincipalIdealRing R] (M : Type v) [AddCommGroup M]
    [Module R M] [Module.Finite R M] :
    ∃ (n : ℕ) (ι : Type u) (_ : Fintype ι) (p : ι → R)
      (_ : ∀ i, Irreducible (p i)) (e : ι → ℕ),
      Nonempty (M ≃ₗ[R] (Fin n →₀ R) ×
        ⨁ i : ι, R ⧸ Submodule.span R {p i ^ e i}) :=
  Module.equiv_free_prod_directSum R M

/-! ### Algebras -/

/-- HP tag 059T (definition-algebra).  A commutative algebra over `R` is a
commutative ring `S` with a ring morphism `R → S`: such a morphism
gives Mathlib's `Algebra R S`. -/
@[reducible] def algebraOfRingHom {S : Type v} [CommRing S] (f : R →+* S) :
    Algebra R S :=
  f.toAlgebra

/-- HP tag 059U (definition-finite-type), item 1.  `S` is of finite type
over `R` if and only if there is a surjection of `R`-algebras
`R[x₁, …, xₙ] → S`. -/
theorem finiteType_iff {S : Type v} [CommRing S] [Algebra R S] :
    Algebra.FiniteType R S ↔
      ∃ (n : ℕ) (f : MvPolynomial (Fin n) R →ₐ[R] S),
        Function.Surjective f :=
  Algebra.FiniteType.iff_quotient_mvPolynomial''

/-- HP tag 059U (definition-finite-type), item 2, in Mathlib's form.  `S` is
of finite presentation over `R` if and only if there is a surjection
`R[x₁, …, xₙ] → S` with finitely generated kernel.

HP asks for an isomorphism `R[x₁, …, xₙ] / (f₁, …, fₘ) ≅ S`; that this
is the same condition is not proved here. -/
theorem finitePresentation_iff {S : Type v} [CommRing S] [Algebra R S] :
    Algebra.FinitePresentation R S ↔
      ∃ (n : ℕ) (f : MvPolynomial (Fin n) R →ₐ[R] S),
        Function.Surjective f ∧ (RingHom.ker f.toRingHom).FG :=
  ⟨fun h => h.out, fun h => ⟨h⟩⟩

/-! ### Spectrum of a ring -/

/-- HP tag 08DK (definition-spectrum-ring), item 2.  `V(T)` is the set of
primes containing `T`; it is Mathlib's `PrimeSpectrum.zeroLocus T`.
The spectrum of item 1 is `PrimeSpectrum R` and the maximal spectrum
of item 4 is `MaximalSpectrum R`. -/
theorem mem_zeroLocus_iff (T : Set R) (p : PrimeSpectrum R) :
    p ∈ PrimeSpectrum.zeroLocus T ↔ ∀ f ∈ T, f ∈ p.asIdeal := by
  rw [PrimeSpectrum.mem_zeroLocus]
  exact Iff.rfl

/-- HP tag 08DK (definition-spectrum-ring), item 3.  `D(f)` is the set of
primes not containing `f`; it is Mathlib's
`PrimeSpectrum.basicOpen f`. -/
theorem mem_basicOpen_iff (f : R) (p : PrimeSpectrum R) :
    p ∈ PrimeSpectrum.basicOpen f ↔ f ∉ p.asIdeal :=
  PrimeSpectrum.mem_basicOpen f p

/-! ### Localization -/

/-- HP tag 059W (definition-localization).  In the localization of `R` at
`S`, `r / s = r₁ / s₁` if and only if `t (s₁ r) = t (s r₁)` for some
`t` in `S`.

HP gave the condition `r s₁ = r₁ s` and asked to check it when `R` has
zero divisors; the factor `t` is what is needed then.  Corrected in HP
on 24 November 2026. -/
theorem localization_mk_eq_mk_iff (S : Submonoid R) (r r₁ : R)
    (s s₁ : S) :
    Localization.mk r s = Localization.mk r₁ s₁ ↔
      ∃ t : S, (t : R) * (s₁ * r) = t * (s * r₁) :=
  Localization.mk_eq_mk_iff.trans Localization.r_iff_exists

/-- HP tag 059W (definition-localization), for a domain.  If `R` is a
domain and `0 ∉ S`, then `r / s = r₁ / s₁` if and only if
`r s₁ = r₁ s`, as in HP's first wording. -/
theorem localization_mk_eq_mk_iff_of_isDomain [IsDomain R]
    (S : Submonoid R) (h0 : (0 : R) ∉ S) (r r₁ : R) (s s₁ : S) :
    Localization.mk r s = Localization.mk r₁ s₁ ↔
      r * s₁ = r₁ * s := by
  rw [localization_mk_eq_mk_iff]
  constructor
  · rintro ⟨t, ht⟩
    have ht0 : (t : R) ≠ 0 := fun h => h0 (h ▸ t.2)
    have := mul_left_cancel₀ ht0 ht
    linear_combination this
  · intro h
    exact ⟨1, by rw [mul_comm (s₁ : R) r, mul_comm (s : R) r₁, h]⟩

/-- HP tag 059Y (lemma-localization-nilpotent).  If `R[1/f] = 0` then `f` is
nilpotent. -/
theorem isNilpotent_of_subsingleton_away (f : R)
    [Subsingleton (Localization.Away f)] : IsNilpotent f := by
  have h := (IsLocalization.subsingleton_iff
    (M := Submonoid.powers f) (S := Localization.Away f)).1
    inferInstance
  obtain ⟨n, hn⟩ := (Submonoid.mem_powers_iff _ _).1 h
  exact ⟨n, hn⟩

/-- HP tag 059Z (exercise-local-noeth-noeth).  A localization of a
Noetherian ring is Noetherian. -/
theorem isNoetherianRing_localization (S : Submonoid R)
    [IsNoetherianRing R] : IsNoetherianRing (Localization S) :=
  IsLocalization.isNoetherianRing S _ inferInstance

end HeapProject.CommutativeAlgebra
