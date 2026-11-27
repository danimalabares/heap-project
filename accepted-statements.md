# Accepted statements

Results Daniel currently accepts without
having worked through their proofs.
This is a learning log, not a claim that
the notes already contain complete proofs.
Every entry must link to its supporting
HP or daniel development and record its
current state, even if only a title exists.

## 2026-10-09 — Deformation theory

### 1. T¹ parametrizes first-order deformations

**Status:** accepted; proof pending study.

For a finitely generated commutative
k-algebra R over a field k,

$$
T^1_{R/k}=\operatorname{Ext}^1_R(L_{R/k},R)
$$

parametrizes isomorphism classes of flat
deformations over the dual numbers, with
a chosen identification of the special
fibre with R. Isomorphisms must respect
that identification.

**Use:** interpret a T¹ class as an
infinitesimal deformation direction.

**Development:** [Why T¹ parametrizes first-order deformations](https://github.com/danimalabares/heap-project/blob/main/deformations.tex#L500).
Partial development; the proof is unfinished.
Stable LaTeX label:
section-first-order-algebra-deformations.

### 2. T² contains obstruction classes

**Status:** accepted; proof pending study.

For R as above,

$$
T^2_{R/k}=\operatorname{Ext}^2_R(L_{R/k},R)
$$

is an obstruction space. Given a small
extension of local Artinian k-algebras
with residue field k,

$$
0\longrightarrow J\longrightarrow B'
\longrightarrow B\longrightarrow0,
$$

the obstruction to lifting a flat
deformation over B to B' belongs to

$$
T^2_{R/k}\otimes_k J.
$$

Here small means that the maximal ideal
of B' annihilates J. The obstruction
vanishes if and only if a lift exists.

**Use:** reduce lifting to vanishing of
an obstruction class. This does not say
that every T² class occurs as an
obstruction, or that a lift is unique.

**Development:** [Why T² contains obstruction classes](https://github.com/danimalabares/heap-project/blob/main/deformations.tex#L769).
Currently a section title only.
Stable LaTeX label: section-obstruction-classes.

### 3. AC multigrading is the torus weight decomposition

**Status:** accepted; construction of the
induced action and decomposition pending
study.

For a complex Stanley–Reisner algebra,
independent variable rescaling induces an
algebraic torus action on T². The AC
multidegree pieces are its weight spaces:

$$
T^2=\bigoplus_{\alpha\in\mathbb{Z}^n}
T^2_\alpha,
$$

$$
T^2_\alpha=
\{v:t\cdot v=t^\alpha v
\ \forall t\in T\},
\qquad
t^\alpha=\prod_{i=1}^n t_i^{\alpha_i}.
$$

The same interpretation holds for T¹.
The torus is not semisimple; algebraic
torus representations split into weight
spaces.

We also accept the compatibility with
vertex permutations used in the notes.
For the chosen automorphism subgroup G,
with g(x_i)=x_{g(i)},

$$
g(T^2_\alpha)=T^2_{g\alpha},
\qquad
(g\alpha)_i=\alpha_{g^{-1}(i)}.
$$

**Use:** organize the AC calculation by
G-orbits of weights. A weight stabilizer
may act nontrivially on its weight
space; this action must be computed.

For the graded projective problem, use
the total-degree-zero part:

$$
(T^2)_0=
\bigoplus_{\sum_i\alpha_i=0}T^2_\alpha.
$$

**Developments:**

- [Weight decomposition for algebraic tori](https://github.com/danimalabares/heap-project/blob/main/representation-theory.tex): definition, decomposition theorem (proof postponed), and differentiation bridge to Lie algebra weights. Labels: section-torus-weights and theorem-torus-weights.
- [Lie algebra weight spaces](https://github.com/danimalabares/heap-project/blob/main/lie-algebras.tex#L401): the familiar simultaneous-eigenvector definition. Label: definition-weight-space.
- [Torus action and AC multidegrees](https://www.heap-project.org/tag/09EL): application to T² and explanation of permutation compatibility. Label: section-torus-action-ac-multidegrees.

The general decomposition is standard
representation theory. AC's contribution
is the combinatorial computation of the
cotangent cohomology pieces; those
formulas have not yet been developed in
this HP section.

The descent of rescaling to a monomial
quotient is already proved there.
These accepted facts do not themselves
prove invariant obstruction vanishing,
equivariant lifting, or smoothness.

### Source for the accepted torus theorem

J. S. Milne, [Algebraic Groups (2022)](https://www.jmilne.org/math/Books/iAG2022.pdf),
Theorem 12.12, printed pages 234–235,
proves the weight decomposition, including
infinite-dimensional algebraic representations.
Corollary 4.8 gives local finiteness;
Section 4g develops characters and eigenspaces.
These references support the general torus
statement, not the construction of the
induced action on cotangent cohomology.
