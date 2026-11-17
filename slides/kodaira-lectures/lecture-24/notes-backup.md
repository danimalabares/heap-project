# Lecture 24 — Nadel to embedding and Kawamata–Viehweg

Monday 16 November 2026. **59 main slides + 4 optional appendix slides.**
Prepared against the current lecture-23 source at tmp commit a42fa4c and Daniel's supplied recording, `New Recording 3.m4a` (75:56.779).

## Actual checkpoint from lecture 23 (Daniel)

The recording starts during Fubini–Study positivity, so it does not establish the duration or coverage of the opening recap. Approximate recording-relative checkpoints, checked against the automatic transcript and current source:

- 00:00–05:45: Fubini–Study positivity and discussion of the unitary-invariance alternative.
- 05:45–12:15: embedding statement, geometric conditions, evaluation sequence; detailed point/jet implications explicitly deferred to the next class.
- 12:15–18:15: smooth Kodaira vanishing, using omega=iTheta and the Lefschetz commutator.
- 18:15–21:15: Nadel statement and historical pause.
- 21:15–41:30: subharmonic/psh reminders, local integrability, singular metrics and curvature.
- 41:30–57:50: multiplier ideal and the radial integrability calculation.
- Around 57:50–60:50: a requested break; ASR on this quiet stretch is unreliable.
- 60:50–66:25: ideal thresholds and the algebra of m_x and m_x^2.
- 66:25–75:15: weighted Dolbeault resolution, Hilbert-space criterion, analytic inputs, Nadel conclusion.
- 75:20–end: metric construction left for Monday; Daniel specifically asks why high powers help.

Thus Monday should use Nadel, rather than repeat its proof. The first three recap slides explicitly retain the analytic inputs as inputs. Raw ASR is private and separate from this public repository; terms, formulas and distant voices are unreliable and have not been silently corrected into purported quotations.

## Priority for Monday, after Daniel's recording review

**Main deck: 54 slides, ending with Chow. Optional continuation: 32 slides in lecture-24-appendix.tex/pdf.** The optional deck contains divisors, degree and Kawamata–Viehweg, together with technical backup slides. Completing KV is not a requirement. The title is *Kodaira embedding theorem (Part 2)*, with subtitle *From solving dbar to homogeneous polynomial equations*.

## Weak spots identified from the recording

- Approximately 56–62 minutes: the strict integrability threshold and the roles of a, n and k become hard to keep track of around the break. Repair with explicit substitutions a=n and a=n+1, and the concrete C² thresholds a=2 and a=3. At equality the integral diverges. Say order **at least** one/two, rather than exactly one/two.
- Approximately 63–66 minutes: the algebra of m_x and m_x² is present, but the significance of the quotient and the differential-geometric immersion conclusion need a separate return. Distinguish the ideal (errors discarded) from the quotient (first-jet data retained).
- Approximately 40–41 and 68–69 minutes: weak derivatives and current positivity were explicitly left unclear. Explain the definition of weak differentiation briefly. For degree zero use the standard regularity fact that a locally integrable distributional dbar-closed function is holomorphic. The multiplier-ideal part of the kernel identity is then the definition, not another deep theorem.
- Approximately 69–71 minutes: distinguish local exactness of a resolution from global solvability. Fineness allows the global complex to compute sheaf cohomology; it alone does not make that cohomology vanish.
- Approximately 71:45–75:10: the Hilbert-space lemma and the analytic estimate carry the argument but are handled rapidly. The old density argument did not establish closed range. The new main slides construct an actual solution using a bounded functional and Riesz representation.
- The final question, around 75:35: why powers help. Preserve the additive curvature calculation and the same-N argument. The singular L2 existence theorem and weighted local lemma stay named analytic inputs.

These times are recording-relative and approximate; the raw ASR is fallible and is not quoted verbatim. The recording starts during Fubini–Study, so it does not establish how long the unrecorded opening lasted.

## Main route and suggested timing

| Slides | Purpose | Minutes |
| --- | --- | ---: |
| 1–5 | Destination and recap | 5 |
| 6–10 | Repair the ideal thresholds and first jets | 8 |
| 11–21 | Kernel identity, weak derivatives, resolution, Hilbert-space proof | 24 |
| 22–23 | Explain the correction s=chi t-u directly | 4 |
| 24–39 | Construct the global metrics and check one exponent | 20 |
| 40–46 | Values, first jets and immersion: finish embedding | 10 |
| 47–54 | Chow proof sketch and the algebraic conclusion | 11 |

This is an 82-minute exposition proposal, leaving about eight minutes for questions in a 90-minute slot. It is not a rehearsal measurement. The real stop rule is clarity, not completion of optional KV. If discussion runs long, keep Chow's statement and the hypersurface/Hartogs mechanism, and summarize the higher-codimension projection as a sketch. The projection lemma and proper-image theorem are not proved in this lecture.

## The Hilbert-space argument, with domain details

Take complex inner products linear in the first variable. Let T:H1→H2 and S:H2→H3 be closed densely defined operators, with im T contained in ker S. Assume C||v||² ≤ ||T*v||²+||Sv||² on Dom T* intersect Dom S, C>0. For f in ker S we prove Tu=f, not f=0.

K=ker S is closed because S is closed. For v in Dom T*, write v=v1+v2 with v1 in K and v2 perpendicular to K. For every a in Dom T, (Ta,v2)=0 since Ta lies in K. By the definition of adjoint, v2 is in Dom T* and T*v2=0. Thus v1 is in Dom T* and, since it belongs to K, in Dom S with Sv1=0. The estimate gives sqrt(C)||v1||≤||T*v||.

Because f lies in K, |(v,f)|=|(v1,f)|≤||f|| ||T*v||/sqrt(C). Hence ell(T*v)=(v,f) is a well-defined bounded linear functional on ran T*. Extend it continuously to its closure and by zero on its orthogonal complement. Riesz produces u with (T*v,u)=(v,f) for every v in Dom T*, and ||u||≤||f||/sqrt(C). By the adjoint definition u belongs to Dom (T*)* and (T*)*u=f. Closedness and dense definition give (T*)*=T. This is the desired actual solution. No unproved assertion that a dense range is closed is used.

This functional-analysis deduction is checked against the orthogonal-projection/Hahn–Banach argument in Demailly, CIME notes, Theorem 5.1, pp. 31–32. The new slides use extension by orthogonal complement plus Riesz instead of naming Hahn–Banach. Singular-weight solvability is still an analytic input; do not assert a classical BKN identity directly for a singular current.

## The direct section correction

Set A=K_X tensor B. Near the prescribed points choose local holomorphic sections t with the required values/jets, and cut them off to a global smooth section t-tilde. The error f=dbar(t-tilde) is dbar-closed and supported away from all poles, so it is weighted L2. Solve dbar u=f with a weighted L2 solution. Near the points f=0; regularity makes u holomorphic there, and its integrability places its coefficient in I(h). Thus subtracting u preserves the chosen values/jets and makes s=t-tilde-u globally holomorphic. The local model t itself need not be weighted L2 at a pole; only the error and the correction need that property.

## Chow: correction and scope of the sketch

Read directly in HP complex-geometry.tex: section-chow-theorem, exercise-pic-of-pn-is-z, theorem-secti-od-degre-d-homog-poly. Cross-checked against Mirko Mauri, *Kodaira Embedding Theorem* (2015), Section 12, Theorems 12.1–12.4, pp. 20–21.

- A **hypersurface**, not an arbitrary submanifold, gives one line bundle with one defining section. Local equations up to units define O(Y) and its canonical section.
- Pic(P^M)=Z uses the exponential sequence **and** H1(O)=H2(O)=0, plus H2(P^M,Z)=Z with O(1) as generator. For M=0 the assertion needed for Chow is trivial.
- Hartogs belongs in the sections-to-polynomials step: lift a section to a homogeneous holomorphic function on C^(M+1) minus the origin, extend it, and compare homogeneous Taylor terms. It is not the reason every higher-codimension submanifold is the zero locus of one section.
- Higher codimension uses a projection separating an exterior point from Y. State the generic-projection fact and analyticity of the proper image as inputs (the latter is Remmert's theorem), rather than claiming that being a closed image alone makes it analytic. Work component by component if Y is reducible; there are finitely many components by compactness and local finiteness.
- Each exterior point can then be excluded by a homogeneous polynomial. The Hilbert basis theorem makes the resulting homogeneous ideal finitely generated. This is a set-theoretic algebraicity conclusion, with no claim that Y is a hypersurface or a complete intersection.

## Small speaking corrections

A cohomology class, not every differential form, has a harmonic representative. In Nadel the closed representative is shown exact, not necessarily zero. In u=sum z_i g_i, the correct relation is g_i(0)=partial_i u(0), not equality of the functions g_i and partial_i u. When the metric is smooth locally, use boundedness above and below of its positive frame norm to justify that it does not change the integrability ideal.

## Optional continuation: audience background

Before KV, the separate appendix defines Div(X) as integer sums of irreducible hypersurfaces, effectiveness, zero divisors of holomorphic sections, degree on a curve, degree with a chosen projective hyperplane class, and the divisor line bundle with its canonical section. Do not treat divisors on an n-fold as if a single unspecified degree or a numerical two-divisor intersection always existed. Only then introduce nef/big and the fixed-divisor/root construction. There is no obligation to present this continuation on Monday.

## Reference and scope checks

Checked directly in Demailly, *L2 Vanishing Theorems for Positive Line Bundles and Adjunction Theory*, arXiv:alg-geom/9410022v3: Theorem 5.11 (Nadel), Corollaries 5.12–5.13 (lifting/jet mechanism), Exercise 5.14 and Theorem 5.15 (embedding), Proposition 6.6(f) proof (ample part), Proposition 6.2(b) (nef plus ample) and Corollary 6.8 (nef and big with mild singularities). The fixed-divisor/root presentation is the existing course route, checked mathematically against those inputs. The KV statement here is the integral line-bundle version on a smooth projective complex variety, not the general log-pair/Q-divisor theorem.

In the weighted Nadel proof, use the singular-weight solvability theorem. Do not assert that a singular curvature current can simply be diagonalized or substituted as a smooth Kähler form. In the smooth Kodaira proof the choice omega=iTheta remains valid and requires no eigenvalue computation.

## Optional details

The following expands the short arguments and records the precise hypotheses. It is not an additional slideshow.

## Embedding details

Fix a Kähler form and positive metric on L; a positive curvature form on the initial compact complex manifold already provides such a Kähler form. A smooth metric on K_X^(-1) has curvature bounded below by -C_0ω. Use B_N=L^N⊗K_X^(-1) for Nadel: applying Nadel directly to L^N would leave an unwanted K_X factor.

Choose a finite atlas V_i compactly contained in U_i, with the V_i covering X. There is a radius ρ_i>0 such that Euclidean balls of radius 2ρ_i about all centres in V_i lie in U_i. Translate a fixed radial cutoff at that radius. On its transition annulus, derivatives of χ and log|z-z(x)| are uniformly bounded. The coordinate metrics are uniformly comparable with ω on the compact chart closures. This supplies a bound independent of x.

For pairs x≠y, sum two weights with coefficient n. Their supports **need not be disjoint**. The weight centred at y is smooth in some neighbourhood of x, however close the points are; hence it does not change the germ ideal at x. The curvature lower bound is at worst the sum of two uniform bounds. For jets use coefficient n+1. One N therefore works simultaneously for every x, every pair, and every first jet. Compactness of X×X minus the diagonal is neither true nor needed.

The value/jet separation proof is explicitly worked out on main slides 40–46: once the uniform metrics give H1-vanishing, the complete linear system is an injective immersion, and compactness makes it a holomorphic embedding. Projectivity in the algebraic sense follows from Chow's theorem, if that identification is not taken as the definition.

The positivity/ample equivalence is used only after proving embedding, so using an ample M_N to choose a positive metric later is not circular.

## Kawamata–Viehweg details

We prove the integral line-bundle version on a smooth projective complex variety. This is not the full Q-divisor/log-pair formulation.

Nef means nonnegative degree on every curve, equivalently membership in the closure of the ample cone in this projective setting. Use the established projective result nef+ample=ample. Do not replace nef by existence of a smooth semipositive metric, and do not claim that strict positivity on all curves alone implies ampleness in general.

Choose A smooth and very ample (Bertini). For the growth bound on A, choose a sufficiently positive line bundle H on A so that H tensor (L|A)^(-1) has a section that vanishes on no component. Its powers inject (L|A)^m into H^m. The Hilbert polynomial of H then gives O(m^(n-1)); these are additional explicit projective inputs in the draft, not implicitly attributed to an unverified earlier lecturer. The dimension argument only needs a subsequence of m along which h^0(L^m)≥c m^n. Its kernel supplies a nonzero section of L^d(-A), with zero divisor D. For curves, A is a finite reduced set and the same bound is O(1). The dimension-zero case is immediate.

**Keep D fixed.** For N>d, M_N=L^(N-d)⊗O(A) is ample, and L^N=M_N⊗O(D). The metric (h_N h_D)^(1/N) has strict curvature lower bound ε_Nω. ε_N may tend to zero; the theorem needs just one chosen positive value.

With h(e,e)=exp(-2φ), Poincaré–Lelong is i∂∂bar log|f|²=2π[div(f)]. Therefore the divisor metric |f_D|^(-2) has curvature 2π[D]. These factors of 2 and π are consistent throughout both drafts.

For the general integrability lemma, choose a coordinate w for which f is Weierstrass regular after a linear coordinate change. Preparation expresses f as a unit times a monic polynomial of degree k. On a smaller polydisc the unit and its reciprocal are bounded, and all roots are uniformly bounded. For each fixed z', factor the polynomial in w; the roots need not be holomorphic functions of z'. Hölder bounds the w-integral when ck<1 by uniform translated-disc integrals. Fubini completes the local proof. A finite cover of the compact divisor gives one exponent. If D is empty the ideal is automatically trivial.

## What we use from the course

Nadel: lecture 23 (Daniel). Chern curvature, psh weights, currents, and Poincaré–Lelong enter the metric constructions. Dolbeault/cohomology enters through Nadel and the long exact sequence. Holomorphic convexity is not an additional step in either application once Nadel is available.

Known speaker attributions are retained when seminar lecture numbers are mentioned; no assignments for other lectures have been guessed.
