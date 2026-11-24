/-
Heap Project, Commutative Algebra, Sections "Noetherian and Artinian
rings" and "Tensor product".

Each declaration carries the permanent HP tag of the statement it
formalizes (https://www.heap-project.org/tag/TAG).  Statements and
proofs were written by Claude Code from `commutative-algebra.tex`; a
proof here certifies the Lean statement, so the match between the Lean
statement and the HP statement has to be checked by a human.
-/
import Mathlib.Algebra.Module.Projective
import Mathlib.LinearAlgebra.LeftExact
import Mathlib.LinearAlgebra.TensorProduct.Quotient
import Mathlib.LinearAlgebra.TensorProduct.RightExactness
import Mathlib.RingTheory.Artinian.Module
import Mathlib.RingTheory.Finiteness.Projective
import Mathlib.RingTheory.Nilpotent.Lemmas
import Mathlib.RingTheory.Noetherian.Basic
import Mathlib.RingTheory.Polynomial.Basic
import Mathlib.RingTheory.PowerSeries.Ideal
import Mathlib.RingTheory.TensorProduct.Basic

namespace HeapProject.CommutativeAlgebra

open TensorProduct

variable {R : Type*} [CommRing R]

/-! ### Noetherian and Artinian rings -/

/-- HP tag 05A1 (definition-noetherian-artinian-rings), Noetherian.  A ring
is Noetherian if and only if every increasing chain of ideals
stabilizes. -/
theorem isNoetherianRing_iff_chain :
    IsNoetherianRing R ↔
      ∀ f : ℕ →o Ideal R, ∃ n, ∀ m, n ≤ m → f n = f m :=
  (monotone_stabilizes_iff_noetherian (R := R) (M := R)).symm

/-- HP tag 05A1 (definition-noetherian-artinian-rings), Artinian.  A ring
is Artinian if and only if every decreasing chain of ideals
stabilizes. -/
theorem isArtinianRing_iff_chain :
    IsArtinianRing R ↔
      ∀ f : ℕ →o (Ideal R)ᵒᵈ, ∃ n, ∀ m, n ≤ m → f n = f m :=
  (monotone_stabilizes_iff_artinian (R := R) (M := R)).symm

/-- HP tag 05A2 (exercise-noeth-iff-ideal-finit-gene).  A ring is Noetherian
if and only if all its ideals are finitely generated. -/
theorem isNoetherianRing_iff_fg :
    IsNoetherianRing R ↔ ∀ I : Ideal R, I.FG :=
  isNoetherianRing_iff_ideal_fg R

/-- HP tag 05A3 (theorem-hilbert-basis) (Hilbert basis theorem).  If `R` is
Noetherian then so is `R[x]`. -/
theorem isNoetherianRing_polynomial [IsNoetherianRing R] :
    IsNoetherianRing (Polynomial R) :=
  inferInstance

/-- HP tag 05A4 (exercise-hilbe-basis-forma-power).  If `R` is Noetherian
then so is `R[[t]]`. -/
theorem isNoetherianRing_powerSeries [IsNoetherianRing R] :
    IsNoetherianRing (PowerSeries R) :=
  inferInstance

/-- HP tag 05A5 (exercise-radical-intersection-primes).  The radical of an
ideal is the intersection of all primes containing it. -/
theorem radical_eq_sInf_prime (I : Ideal R) :
    I.radical = sInf {J : Ideal R | I ≤ J ∧ J.IsPrime} :=
  Ideal.radical_eq_sInf I

/-- HP tag 08DN (exercise-intersection-submodules-noet).  If `N₁ ∩ N₂ = 0`
and `M / N₁`, `M / N₂` are Noetherian then `M` is Noetherian. -/
theorem isNoetherian_of_quotients {M : Type*} [AddCommGroup M]
    [Module R M] (N₁ N₂ : Submodule R M) (h : N₁ ⊓ N₂ = ⊥)
    [IsNoetherian R (M ⧸ N₁)] [IsNoetherian R (M ⧸ N₂)] :
    IsNoetherian R M := by
  refine isNoetherian_of_injective (N₁.mkQ.prod N₂.mkQ) ?_
  rw [← LinearMap.ker_eq_bot, LinearMap.ker_prod, Submodule.ker_mkQ,
    Submodule.ker_mkQ, h]

/-- HP tag 08DP (exercise-descending-chains-is-field).  A domain in which
every descending chain of ideals stabilizes is a field. -/
theorem isField_of_isDomain_of_isArtinianRing [IsDomain R]
    [IsArtinianRing R] : IsField R :=
  IsArtinianRing.isField_of_isDomain R

/-! ### Tensor product -/

section Tensor

variable {M₁ M₂ M₃ M N : Type*} [AddCommGroup M₁] [Module R M₁]
  [AddCommGroup M₂] [Module R M₂] [AddCommGroup M₃] [Module R M₃]
  [AddCommGroup M] [Module R M] [AddCommGroup N] [Module R N]

/-- HP tag 05A8 (theorem-unive-prope-tenso-produ) (universal property of the
tensor product).  For a bilinear map `B : M₁ × M₂ → M` there is a
unique linear map `b : M₁ ⊗ M₂ → M` with `b (m₁ ⊗ m₂) = B (m₁, m₂)`.
Bilinear maps are written `M₁ →ₗ M₂ →ₗ M`, as in Mathlib. -/
theorem existsUnique_lift (B : M₁ →ₗ[R] M₂ →ₗ[R] M) :
    ∃! b : M₁ ⊗[R] M₂ →ₗ[R] M, ∀ m₁ m₂, b (m₁ ⊗ₜ m₂) = B m₁ m₂ :=
  ⟨TensorProduct.lift B, fun _ _ => TensorProduct.lift.tmul _ _,
    fun b hb => TensorProduct.ext' fun m n => by
      rw [hb, TensorProduct.lift.tmul]⟩

/-- HP tags 05AA (remark-universal-property) and 05AB (exercise-currying).
Linear maps `M₁ ⊗ M₂ → M` correspond bijectively to bilinear maps
`M₁ × M₂ → M`, that is, to linear maps `M₁ → Hom(M₂, M)`. -/
theorem lift_bijective :
    Function.Bijective
      (fun B : M₁ →ₗ[R] M₂ →ₗ[R] M => TensorProduct.lift B) := by
  constructor
  · intro B B' h
    refine LinearMap.ext₂ fun m n => ?_
    have := congrArg (fun b : M₁ ⊗[R] M₂ →ₗ[R] M => b (m ⊗ₜ n)) h
    simpa using this
  · intro b
    exact ⟨(TensorProduct.mk R M₁ M₂).compr₂ b,
      TensorProduct.ext' fun m n => by simp⟩

/-- HP tag 05AC (exercise-left-hom-sends-right-exact).  If
`M₁ → M₂ → M₃ → 0` is exact then
`0 → Hom(M₃, N) → Hom(M₂, N) → Hom(M₁, N)` is exact. -/
theorem hom_left_exact {f₁ : M₁ →ₗ[R] M₂} {f₂ : M₂ →ₗ[R] M₃}
    (h : Function.Exact f₁ f₂) (hs : Function.Surjective f₂) :
    Function.Injective (LinearMap.lcomp R N f₂) ∧
      Function.Exact (LinearMap.lcomp R N f₂)
        (LinearMap.lcomp R N f₁) := by
  refine ⟨fun g g' e => LinearMap.ext fun y => ?_,
    by apply LinearMap.exact_lcomp_of_exact_of_surjective <;> assumption⟩
  obtain ⟨x, rfl⟩ := hs y
  exact LinearMap.congr_fun e x

/-- HP tag 05AH (definition-projective-module).  A projective module has
the lifting property of the diagram in HP: a map `N → M₃` lifts along
any surjection `M₂ → M₃`. -/
theorem projective_lifting [Module.Projective R N]
    (f : M₂ →ₗ[R] M₃) (g : N →ₗ[R] M₃)
    (hf : Function.Surjective f) :
    ∃ h : N →ₗ[R] M₂, f ∘ₗ h = g :=
  Module.projective_lifting_property f g hf

/-- HP tag 05AM (theorem-tensor-product-is-right-exact).  If
`M₁ → M₂ → M₃ → 0` is exact then so is
`M₁ ⊗ M → M₂ ⊗ M → M₃ ⊗ M → 0`. -/
theorem tensor_right_exact {f₁ : M₁ →ₗ[R] M₂} {f₂ : M₂ →ₗ[R] M₃}
    (h : Function.Exact f₁ f₂) (hs : Function.Surjective f₂) :
    Function.Exact (f₁.rTensor M) (f₂.rTensor M) ∧
      Function.Surjective (f₂.rTensor M) :=
  ⟨rTensor_exact M h hs, LinearMap.rTensor_surjective M hs⟩

/-- HP tag 05AP (proposition-tensor-ideals).  For an ideal `I`,
`M ⊗ (R / I) = M / I M`. -/
noncomputable def tensorQuotientEquiv (I : Ideal R) :
    (M ⊗[R] (R ⧸ I)) ≃ₗ[R] M ⧸ (I • (⊤ : Submodule R M)) :=
  TensorProduct.tensorQuotEquivQuotSMul M I

/-- HP tag 05AR (definition-tensor-product-of-rings).  The product on
`A ⊗ B` satisfies `(a ⊗ b) (a' ⊗ b') = a a' ⊗ b b'`. -/
theorem tmul_mul_tmul {A B : Type*} [CommRing A] [CommRing B]
    [Algebra R A] [Algebra R B] (a a' : A) (b b' : B) :
    (a ⊗ₜ[R] b) * (a' ⊗ₜ[R] b') = (a * a') ⊗ₜ[R] (b * b') :=
  Algebra.TensorProduct.tmul_mul_tmul a a' b b'

end Tensor

/-- HP tag 05AX (lemma-inter-maxim-ideal-nilra).  The intersection of all
prime ideals of a ring is its nilradical.

HP states this for finitely generated complex algebras; it holds for
every commutative ring. -/
theorem nilradical_eq_sInf_prime :
    nilradical R = sInf {J : Ideal R | J.IsPrime} :=
  nilradical_eq_sInf R

end HeapProject.CommutativeAlgebra
