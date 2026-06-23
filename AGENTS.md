# AGENTS.md

Repository guidance for AI agents working in
this repo. Follow this rules when
editing any heap-project file!!!!

- Do not use any macros at all.
- Do not write text in equations.
  Write in prose whatever you need to explain
  and put only formulas in equations.

- Do not use `align*`. For unnumbered aligned displays, use:

  ```tex
  $$
  \begin{aligned}
  A &= B \\
    &= C
  \end{aligned}
  $$
  ```

- For numbered aligned displays, use:

  ```tex
  \begin{equation}
  \begin{aligned}
  A &= B \\
    &= C
  \end{aligned}
  \end{equation}
  ```

- Maximum linewidth is 45 characters.
- Do not write inner products with raw 
  angle brackets like `\left< X,Y \right>`. 
  Use `\left\langle{} X,Y \right\rangle{}` 
  instead.
- Do not use `\subsetneq`; use `\subset` 
- instead.
- Do not use `\supsetneq`; use `\supset` 
  instead.
- In every `definition` environment, 
  italicize the term being defined.
- Put corollaries in a `lemma` environment 
  with the optional title
  `[Corollary]`.
- Never use capital letters in LaTeX labels. Use labels like
  `\label{theorem-rauch-clean}` instead of
  `\label{theorem-Rauch-clean}` or
  `\label{section-Hadamard}`. This applies 
  to theorem, lemma,
  proposition, definition, equation, 
  exercise, section, and remark labels.
- Do not globally reformat existing TeX 
  files. Preserve the repo's line wrapping 
  and style.
- Before committing TeX cleanup changes, 
  check that no source `.tex` files contain 
  `\begin{align*}`, `\end{align*}`, 
  `\left<`, or `\right>` outside generated 
  directories like `gerby/` and `tmp/`.
- Do not use subsections or subsubsections.

Generated files and directories such as
`gerby/`, `tmp/`, `.venv/`, and build
artifacts should not be committed.
