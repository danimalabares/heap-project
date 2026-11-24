/-
Heap Project, Commutative Algebra, Section "Flat modules".

Each declaration carries the permanent HP tag of the statement it
formalizes (https://www.heap-project.org/tag/TAG).  Statements and
proofs were written by Claude Code from `commutative-algebra.tex`; a
proof here certifies the Lean statement, so the match between the Lean
statement and the HP statement has to be checked by a human.
-/
import Mathlib.LinearAlgebra.TensorProduct.Pi
import Mathlib.RingTheory.Flat.Localization
import Mathlib.RingTheory.Flat.TorsionFree
import Mathlib.RingTheory.Localization.BaseChange
import Mathlib.RingTheory.LocalRing.Module

namespace HeapProject.CommutativeAlgebra

open TensorProduct

universe u

/-- HP tag 08DU (definition-flat-module).  `M` is flat if and only if
`X ↦ X ⊗ M` is exact: it takes exact sequences to exact sequences. -/
theorem flat_iff_tensor_exact {R : Type u} {M : Type u} [CommRing R]
    [AddCommGroup M] [Module R M] :
    Module.Flat R M ↔
      ∀ ⦃N N' N'' : Type u⦄ [AddCommGroup N] [AddCommGroup N']
        [AddCommGroup N''] [Module R N] [Module R N'] [Module R N'']
        ⦃f : N →ₗ[R] N'⦄ ⦃g : N' →ₗ[R] N''⦄,
        Function.Exact f g →
          Function.Exact (f.rTensor M) (g.rTensor M) :=
  Module.Flat.iff_rTensor_exact

/-- HP tag 09AW (lemma-free-tensor-copies).  `N ⊗ R^r ≅ N^r`. -/
noncomputable def freeTensorCopies (R : Type*) [CommRing R] (N : Type*)
    [AddCommGroup N] [Module R N] (r : ℕ) :
    N ⊗[R] (Fin r → R) ≃ₗ[R] (Fin r → N) :=
  TensorProduct.piScalarRight R R N (Fin r)

/-- HP tag 09AW (lemma-free-tensor-copies), second sentence.  Finite free
modules are flat. -/
theorem flat_of_finite_free (R : Type*) [CommRing R] (r : ℕ) :
    Module.Flat R (Fin r → R) :=
  inferInstance

/-- HP tag 08DV (definition-torsion-module).  For a domain `A` with fraction
field `K`, the kernel of `M → M ⊗ K` is the torsion submodule of `M`
(elements killed by a nonzero element of `A`). -/
theorem ker_toLocalization_eq_torsion (A : Type*) [CommRing A]
    [IsDomain A] (K : Type*) [Field K] [Algebra A K] [IsFractionRing A K]
    (M : Type*) [AddCommGroup M] [Module A M] :
    LinearMap.ker (TensorProduct.mk A K M 1) = Submodule.torsion A M := by
  haveI : IsLocalizedModule (nonZeroDivisors A) (TensorProduct.mk A K M 1) :=
    (isLocalizedModule_iff_isBaseChange (nonZeroDivisors A) K
      (TensorProduct.mk A K M 1)).mpr (TensorProduct.isBaseChange A M K)
  ext x
  simp only [LinearMap.mem_ker]
  rw [IsLocalizedModule.eq_zero_iff (nonZeroDivisors A)]
  rfl

/-- HP tag 08DW (exercise-flat-modules-torsion-free).  A flat module over a
domain is torsion-free. -/
theorem torsion_eq_bot_of_flat (A : Type*) [CommRing A] [IsDomain A]
    (M : Type*) [AddCommGroup M] [Module A M] [Module.Flat A M] :
    Submodule.torsion A M = ⊥ :=
  Module.Flat.torsion_eq_bot

/-- HP tag 08DY (exercise-flat-finite-local-free).  A finitely generated
module over a Noetherian local ring is flat if and only if it is free. -/
theorem flat_iff_free_of_local (R : Type u) [CommRing R] [IsNoetherianRing R]
    [IsLocalRing R] (M : Type u) [AddCommGroup M] [Module R M]
    [Module.Finite R M] : Module.Flat R M ↔ Module.Free R M :=
  ⟨fun _ => Module.free_of_flat_of_isLocalRing, fun _ => inferInstance⟩

/-- HP tag 08DZ (exercise-local-flat-implies-flat).  A module that is flat
over every localization at a maximal ideal is flat.  (HP assumes `A` a
domain; this is not needed.) -/
theorem flat_of_flat_at_maximal (A : Type*) [CommRing A] (M : Type*)
    [AddCommGroup M] [Module A M]
    (Mₚ : ∀ (P : Ideal A) [P.IsMaximal], Type*)
    [∀ (P : Ideal A) [P.IsMaximal], AddCommGroup (Mₚ P)]
    [∀ (P : Ideal A) [P.IsMaximal], Module A (Mₚ P)]
    (f : ∀ (P : Ideal A) [P.IsMaximal], M →ₗ[A] Mₚ P)
    [∀ (P : Ideal A) [P.IsMaximal], IsLocalizedModule.AtPrime P (f P)]
    (H : ∀ (P : Ideal A) [P.IsMaximal], Module.Flat A (Mₚ P)) :
    Module.Flat A M :=
  Module.flat_of_isLocalized_maximal (R := A) (S := A) (M := M) Mₚ f H

end HeapProject.CommutativeAlgebra
