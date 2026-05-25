# AGENTS.md

Repository guidance for AI agents working in this repo.

## Gerby-safe LaTeX rules

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

- Do not write inner products with raw angle brackets like `\left< X,Y \right>`. Use `\left\langle{} X,Y \right\rangle{}` instead.
- Do not use `\subsetneq`; use `\subset` instead.
- Do not use `\supsetneq`; use `\supset` instead.
- In every `definition` environment, italicize the term being defined.
- Never use capital letters in LaTeX labels. Use labels like
  `\label{theorem-rauch-clean}` instead of
  `\label{theorem-Rauch-clean}` or
  `\label{section-Hadamard}`. This applies to theorem, lemma,
  proposition, definition, equation, exercise, section, and
  remark labels.
- Do not globally reformat existing TeX files. Preserve the repo's line wrapping and style.
- Before committing TeX cleanup changes, check that no source `.tex` files contain `\begin{align*}`, `\end{align*}`, `\left<`, or `\right>` outside generated directories like `gerby/` and `tmp/`.

Generated files and directories such as `gerby/`, `tmp/`, `.venv/`, and build artifacts should not be committed.
