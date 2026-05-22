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
- Do not globally reformat existing TeX files. Preserve the repo's line wrapping and style.
- Before committing TeX cleanup changes, check that no source `.tex` files contain `\begin{align*}`, `\end{align*}`, `\left<`, or `\right>` outside generated directories like `gerby/` and `tmp/`.

Generated files and directories such as `gerby/`, `tmp/`, `.venv/`, and build artifacts should not be committed.
