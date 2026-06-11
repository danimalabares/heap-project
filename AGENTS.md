# AGENTS.md

Repository guidance for AI agents working in this repo.

## Gerby-safe LaTeX rules

- Do not add new LaTeX packages to `preamble.tex`,
  chapter files, or Gerby-generated preambles unless the user
  explicitly asks for it. If a command is undefined, first remove
  or rewrite the source usage using already-supported Stacks/HP
  LaTeX. Package additions can break Gerby/plasTeX even when PDF
  compilation succeeds.

- In particular, do not add `xcolor`, `tikz`, `tikz-cd`,
  `cleveref`, or other convenience packages as a compile fix.

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
- Put corollaries in a `lemma` environment with the optional title
  `[Corollary]`.
- Never use capital letters in LaTeX labels. Use labels like
  `\label{theorem-rauch-clean}` instead of
  `\label{theorem-Rauch-clean}` or
  `\label{section-Hadamard}`. This applies to theorem, lemma,
  proposition, definition, equation, exercise, section, and
  remark labels.
- Do not introduce chapter-specific shorthand macros in
  `preamble.tex`. HP should use only the shared Stacks-style macro
  layer.
- Before adding any global macro, compare with the Stacks Project
  preamble and justify that it belongs globally.
- Prefer explicit standard LaTeX in chapter content, e.g.
  `\operatorname{Top}` instead of `\Top` and `\mathbb{C}` instead of
  `\C`.
- Macros in section titles, theorem titles, optional arguments,
  captions, and labels are especially dangerous because they are
  written to `.aux` files and can break unrelated chapters through
  `\externaldocument`.
- If a compile error mentions an undefined macro while reading
  `\externaldocument`, first check for stale `.aux` files and
  unsupported macros in the referenced chapter.
- Do not globally reformat existing TeX files. Preserve the repo's line wrapping and style.
- Before committing TeX cleanup changes, check that no source `.tex` files contain `\begin{align*}`, `\end{align*}`, `\left<`, or `\right>` outside generated directories like `gerby/` and `tmp/`.

Generated files and directories such as `gerby/`, `tmp/`, `.venv/`, and build artifacts should not be committed.
