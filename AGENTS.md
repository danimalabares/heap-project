When editing TeX notes in this repository:

- Keep source lines at 45 characters or less.
- Check edited TeX files with:
  `awk 'length($0)>45' file.tex`
- Preserve the existing short-line style.
- Do not reflow unrelated text unless needed.
- When inserting an abstract, copy it
  literally from the source.
- Use `\mathbb{R}` for the reals, not
  `\mathbf{R}`.
- Do not use `\ltimes` or `\rtimes`;
  write semidirect products in prose or
  with ordinary product notation.
- Some AMS relation symbols are not
  available here. Do not use symbols such
  as `\subsetneq` or `\supsetneq`;
  rewrite them using supported relations.
- Use `\noindent` mainly for paragraphs
  immediately after environments, as in the
  Stacks Project style. Do not add it to
  every paragraph.
- Use proper theorem-style environments
  for theorems, definitions, remarks, and
  examples when possible.
- Every theorem-style environment should
  have a `\label{...}` immediately after
  `\begin{...}`.
- Labels should start with the environment
  name, for example `theorem-...` or
  `lemma-...`.
- Keep labels short and single-line.
  Prefer compact, concept-based labels
  like `theorem-nullstellensatz`.
- The environment types covered by this
  rule include `lemma`, `proposition`,
  `theorem`, `remark`, `remarks`,
  `example`, `exercise`, `situation`,
  `equation`, and `definition`.
- There is no `corollary` environment in
  this project.
- Do not use `\subsection` in these notes.
  Use plain text headings or paragraphs
  instead.

Stacks Project coding conventions to
follow here:

- Do not indent TeX source.
- Start displayed equations with `$$` on
  its own line.
- Prefer no line breaks inside inline
  formulas unless the formula is too long.
- Use `\medskip\noindent` for new
  paragraphs, and `\noindent` directly
  after environments.
- Avoid custom macros.
- Use only these theorem-style
  environments: `theorem`, `proposition`,
  `lemma`, `definition`, `example`,
  `exercise`, `situation`, `remark`,
  `remarks`, `equation`, and `proof`.
- Do not use `corollary`; use `lemma`
  instead.
- Place the proof directly after the
  statement, with no nested proofs.
- Label statements with lower-case tags
  using the environment name as prefix.
- Avoid references like “the lemma above”.
