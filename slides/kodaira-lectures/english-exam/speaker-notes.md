# Speaking notes

Target: **9 minutes** for slides 1–13, with one minute of buffer. The appendix (slides 14–25) is for questions or for reading; it is not part of the timed talk.

Speak slowly. Pause after each boxed formula. Short sentences are easier to say clearly than long ones.

| Slide | Time | Cumulative |
| --- | ---: | ---: |
| 1. Title | 0:20 | 0:20 |
| 2. The plan | 0:25 | 0:45 |
| 3. Fubini–Study is positive | 1:00 | 1:45 |
| 4. Positivity passes to submanifolds | 0:40 | 2:25 |
| 5. Kodaira embedding theorem | 0:40 | 3:05 |
| 6. Kodaira | 0:25 | 3:30 |
| 7. History | 0:45 | 4:15 |
| 8. Sections give a map | 0:45 | 5:00 |
| 9. Three conditions | 0:40 | 5:40 |
| 10. Lifting problem | 0:55 | 6:35 |
| 11. Hodge theory | 0:40 | 7:15 |
| 12. Bochner–Kodaira | 1:05 | 8:20 |
| 13. Summary | 0:40 | 9:00 |

## 1. Title

"Good morning. Today I will talk about Kodaira's embedding theorem. It says that positive curvature gives coordinates."

## 2. The plan

"The plan has three steps. First, projective space carries a positive form, the Fubini–Study form. Second, Kodaira's theorem is the converse of this fact. Third, I will sketch the proof. The key idea is that harmonic forms must vanish."

## 3. Projective space has a positive form

"A point of projective space is a line through the origin. So we identify two tuples when one is a multiple of the other. In a chart, the Fubini–Study form is i over two pi, times d d-bar of the logarithm of one plus the norm of z squared. If we evaluate it on a nonzero tangent vector, we get this quotient. By the Cauchy–Schwarz inequality, it is strictly positive. So the Fubini–Study form is positive. It is the curvature of a line bundle called O of one."

## 4. Positivity passes to submanifolds

"Now take a compact complex submanifold of projective space. We restrict the line bundle O of one to it. Its curvature is the restriction of the Fubini–Study form, and a positive form stays positive on a subspace. So every projective manifold has a positive line bundle. The natural question is: is the converse true?"

## 5. Kodaira embedding theorem

"Kodaira answered yes, in nineteen fifty-four. If a compact complex manifold has a line bundle with positive curvature, then the sections of a high power of that bundle embed the manifold into projective space. In short: positive implies projective."

## 6. Kodaira

"This is Kunihiko Kodaira. He received the Fields Medal in nineteen fifty-four for his work on harmonic integrals and their applications to Kähler and algebraic varieties. His idea was that an analytic condition, curvature, produces an algebraic object."

## 7. Where this sits in history

"Where does this theorem sit in history? In eighteen fifty-one, Riemann introduced Riemann surfaces. He used analysis to construct functions, and so he showed that compact Riemann surfaces are algebraic curves. Then came the Fubini–Study metric, Kähler's metrics in nineteen thirty-three, and Hodge's harmonic forms in nineteen forty-one. Kodaira combined all of these. Later, Hörmander made the method much more flexible. The common theme is: analysis produces functions."

## 8. Sections give a map

"Now the proof. We choose a basis of holomorphic sections. In a local frame, each section is a function times the frame. These functions are the coordinates of a point in projective space. If we change the frame, all the coordinates are multiplied by the same number, so the point does not change. This is the canonical map."

## 9. Three conditions

"We need three conditions. First, the sections have no common zero. Then the map is defined everywhere. Second, the sections separate points. Then the map is injective. Third, the sections separate tangent directions. Then the map is an immersion. On a compact manifold, an injective immersion is an embedding."

## 10. Each condition is a lifting problem

"Each condition asks for global sections with prescribed values, or prescribed first derivatives. An exact sequence tells us when this is possible. The obstruction lies in a first cohomology group. If this group is zero, every choice of data lifts to a global section. After a blow-up, which I will not explain, this group has the form H one of K tensor B, where B is positive."

## 11. Hodge theory

"Now we use Hodge theory. On a compact Kähler manifold, every cohomology class has exactly one harmonic representative. So, to show that the cohomology group is zero, it is enough to show that every harmonic form is zero."

## 12. Bochner–Kodaira

"The Bochner–Kodaira formula compares two Laplacians. The difference is a curvature term. If the curvature is positive, this term is at least q times epsilon. Now we take a harmonic form u and integrate. The left side is zero. On the right side, the first two terms are not negative, and the curvature term is at least q epsilon times the norm of u squared. So, when q is positive, u must be zero. This is Kodaira's vanishing theorem."

## 13. Summary

"To summarize. Positive curvature, by Bochner–Kodaira, leaves no harmonic forms. So the first cohomology vanishes. By the exact sequence, we have enough sections. These sections satisfy the three conditions. So they give an embedding into projective space. Thank you."

## Short answers for questions

**Why projective space rather than affine space?** On a compact connected complex manifold, every global holomorphic function is constant. Sections of a line bundle can vary, and their ratios give projective coordinates.

**Why a high power of L?** The curvature of the k-th power is k times the curvature of L. A large k makes it dominate the curvature of the canonical bundle and the blow-up terms.

**Is every compact Kähler manifold projective?** No. A generic complex torus of dimension at least two is Kähler but not projective. Voisin (2004) found Kähler manifolds that are not even homotopy equivalent to projective ones.

**Who was Kähler?** Erich Kähler, a German mathematician. In 1933 he studied Hermitian metrics whose form is closed. Today they carry his name.
