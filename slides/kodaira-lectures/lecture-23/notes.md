# Lecture 23 — the embedding mechanism and Nadel

61 slides. This is the first half of one argument continued in lecture 24 (Daniel). The theorem to keep in view from the beginning is Kodaira embedding.

## Opening: course recap

Spend about three minutes on slides 2–3. The recap follows the supplied 2025 source PDFs from the first class onward. Group the topics by what they gave us, rather than reciting a lecture-by-lecture catalogue.

Suggested spoken transition: “We started by asking what a complex manifold is. We learned how metrics and connections control differential forms, how forms compute cohomology, and how positivity makes cohomology vanish. The analytic chapters let us use singular weights. Now we use all of this to construct a projective embedding.”

The Fubini–Study example already showed projective manifolds are Kähler. Verbitsky's 2025 source PDF on homogeneous Kähler metrics explicitly states Kodaira embedding. The final lectures return to that promised converse. Do not claim every intermediate topic is a direct ingredient: torsion/Bismut supplies geometric background, while the later L2, pseudoconvexity, and psh material supports the analytic extension.

The recap uses topic names without assigning unverified seminar speakers. Confirmed numbered references retain the known names.

## Essential preparation

The main opening argument is now on the slides, not deferred to the next lecture:
1. Sections define a projective map if they have no common zero.
2. Independent prescribed values separate points.
3. Prescribed first jets make the differential injective.
4. Compactness turns an injective immersion into an embedding.
5. The long exact sequence turns all three prescriptions into H1-vanishing.

Then prepare the radial ideal calculation and the weighted Dolbeault argument. State the full singular-weight L2 existence theorem as an analytic input, as before.

## Route

- 2–12: course recap, Fubini–Study, statement of embedding, separating sections and the evaluation sequence.
- 13–18: smooth Kodaira vanishing. Choose the Kähler form to be the curvature of B. The Lefschetz commutator acts by q in bidegree (n,q), so the harmonic form is zero.
- 19–44: Nadel’s statement, singular weights and the radial example giving the desired ideals.
- 45–47: the weighted resolution and the Hilbert-space criterion explain which estimate is needed.
- 48–58: optional detailed proof of the estimate for a smooth metric against an independently fixed background. The button on slide 47 jumps straight to the summary on slide 59.
- 59–61: distinguish the smooth calculation from the singular analytic input, conclude Nadel and set up the metric construction in lecture 24 (Daniel).

## Curvature conventions (2026-11-04 review)

The reminders follow HP complex-geometry.tex (labels definition-connection-vector-bundle and definition-curvature-connection) and geometric-prequantization.tex. The graded extension in Definition 8.12 gives locally d+a wedge. For a line bundle, End(L) is canonically trivial, so curvature is a scalar two-form on X, although the connection takes values in L-valued one-forms. Unitarity makes curvature imaginary; the Chern condition makes it type (1,1). For higher rank, the Bianchi identity is covariant closedness; it is the trace that is an ordinary closed form representing c1.

Use Theta=nabla², h(e,e)=exp(-2φ), and c1(L)_R=[iTheta/(2π)] consistently. HP geometric-prequantization.tex currently writes [Omega/(2πi)] with Omega=nabla², an opposite sign; do not import that mismatch. HP complex-geometry.tex, definition-positive-11form, also swaps the strict/non-strict positivity terminology. Here positive means >0 on nonzero tangent vectors, semipositive means >=0. These discrepancies are flagged for a separate HP correction, not silently changed by the requested cross-reference edit.

The two-fibre target is a vector space of dimension two; as a quotient sheaf it is a sum of skyscraper sheaves, not a rank-two locally free sheaf on X. Injective and immersion are also standard in complex geometry. Base-point freeness and separation express these conditions in the language of sections. Surjectivity onto all first jets is the sufficient condition used here.

The optional smooth model in the Nadel proof diagonalizes iTheta relative to omega. On (n,q)-forms the eigenvalue of the commutator is the sum of the q antiholomorphic curvature eigenvalues. Integration by parts then identifies the Laplacian pairings with squared norms; discard the nonnegative partial-Laplacian term. This is the smooth compact argument, not a substitute for the singular-weight existence theorem.

## Details of the opening mechanism

Write I=m_x for the ideal sheaf of the point, whose stalk is O away from x. The quotient A⊗O/I is the fibre A|_x as a skyscraper sheaf. Its global sections are precisely that fibre. H1(A⊗m_x)=0 therefore gives a global section taking any chosen nonzero value at x.

For x≠y, I=m_x∩m_y has quotient supported at those two points. After choosing fibre coordinates, surjectivity gives sections with values (1,0) and (0,1). The two evaluation functionals cannot be proportional, so the complete linear system separates the points.

For first jets, choose a local frame of A and coordinates centred at x. Surjectivity modulo m_x² yields s_0=1+O(|z|²) and s_j=z_j+O(|z|²). Their projective ratios have differentials dz_j. These sections can be included in a basis of H0(A), or viewed as linear combinations of its projective coordinates. Either way, the differential has rank n.

These are sufficient conditions for Kodaira **embedding**. Kodaira **vanishing** is a cohomological theorem used in the route toward embedding. The cusp is a useful example showing that injectivity alone is insufficient; it is not a classification of failures of immersion.

At this point all implications are conditional on one uniform N. No existence of the needed metrics or vanishing groups has yet been proved. The slide “Nadel now fits the embedding mechanism” explains exactly how Nadel reduces the missing assertion to constructing metrics on B_N, not on A itself.

Historical context, if useful orally: Nadel's 1990 paper developed multiplier ideals in the Kähler–Einstein problem. The published source is linked in sources.md.

## Optional details

The rest is reference material. It need not all be prepared as spoken content.

## Conventions and details to say aloud

We use squared frame norm h(e,e)=exp(-2φ), hence iΘ_h=2i∂∂bar φ. A positive curvature current has locally psh weights after the appropriate smooth potential is subtracted. The local integrability definition alone works more generally, but Nadel needs this curvature hypothesis.

The ideal I_h is a subsheaf of O_X. The integrable holomorphic sections are B⊗I_h; integrable holomorphic top forms with values in B are K_X⊗B⊗I_h. Keep these three objects distinct.

For a nonzero holomorphic germ of order k, angular integration of its Taylor expansion has leading order r^(2k), with a positive leading angular integral. This justifies the radial criterion k+n>a even when the leading polynomial vanishes in some directions. The zero germ is always integrable.

For the degree-zero kernel, the weight is locally bounded above, so weighted L2 implies unweighted local L2. Distributional holomorphicity then gives genuine holomorphicity. The coefficient times dz_1∧…∧dz_n is locally integrable precisely when its coefficient belongs to I_h.

The sheaf domain is u and ∂bar u locally L2. Do not impose an adjoint condition: that is a global Hilbert-space issue, not the fine sheaf we use. The derivative condition is automatic for a closed representative and for a primitive with ∂bar u=f.

## What is proved and what is imported

The slides explain the radial ideal calculation, fineness, and the sheaf-cohomology deduction. Frame independence and the Hilbert-space estimate-to-solution argument are optional preparation details below. Smooth Bochner–Kodaira and smooth Hodge theory are previous inputs.

Two analytic results are explicitly imported:
1. weighted local ∂bar solvability for psh/quasi-psh weights;
2. the global singular-weight L2 existence theorem on compact Kähler manifolds with a strict current lower bound.

The approximation slide is an explanation of the mechanism, **not** a full proof of the second theorem. A general positive singular metric need not be globally smoothable while preserving strict positivity; pretending otherwise would already force false ampleness conclusions. Use the complete-metric/exhaustion and regularization theorem in the analytic reference.

The main talk states these analytic inputs. It does not require presenting the full regularization or functional-analysis proof. The details below are for answering questions or for a later, longer treatment.

## Functional analysis details

Let T and S be closed densely defined operators with ST=0. Z=ker S is closed. Regard T as a closed operator T_0 into Z; its domain is dense in the source. Its adjoint is the restriction of T* to Z. The basic estimate on Dom(T*)∩Dom(S) gives ||v|| ≤ c^(-1/2)||T_0*v|| for v in Dom(T_0*).

Use the inner-product convention linear in the first variable. Define the linear functional ℓ(T_0*v)=〈v,f〉. The lower bound makes T_0* injective, hence ℓ well defined. Hahn–Banach extends it, Riesz represents it by u, and the equality 〈T_0*v,u〉=〈v,f〉 says u lies in Dom(T_0**) and T_0**u=f. Closedness gives T_0**=T_0. No smooth harmonic representative is used in the singular case.

For local approximation, first restrict to a relatively compact ball on which f has finite weighted norm. Fix a strictly positive quadratic correction. Smooth psh approximants decrease on smaller balls, so the norms increase. Uniform estimates give weakly convergent subsequences in each fixed approximating weighted space; diagonal extraction, lower semicontinuity, and monotone convergence produce the limiting weighted bound. Global patching is not accomplished by merely partitioning solutions.

## Previous material

- Kähler identities: lecture 10 (Beatrice), behind the Bochner–Kodaira identity.
- Chern connection: lecture 14 (Yan), behind the meaning of Θ.
- Bochner–Kodaira/Kodaira vanishing: lecture 16 (Vanya).
- Dolbeault, fine resolutions, partitions of unity, distributional ∂bar, psh functions, and currents: used by name. Do not invent unconfirmed seminar speaker assignments.
- Holomorphic convexity is part of the analytic background for Stein/exhaustion methods. It is not a separate algebraic step in the displayed proof of Nadel, and one should not claim that holomorphic convexity by itself supplies the L2 estimate.

The plan deck is intentionally preserved rather than silently rewritten to match this expanded teaching route.
