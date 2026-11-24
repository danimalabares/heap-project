# Heap Project in Lean

Lean 4 formalization of statements of the Heap Project, checked
against Mathlib. One file per HP section, under
`HeapProject/<Chapter>/`. Each declaration's docstring gives the
permanent HP tag of the statement it formalizes
(https://www.heap-project.org/tag/TAG).

A proof here certifies the Lean statement. Whether the Lean
statement says the same as the HP statement is a separate, human
check; departures from the HP wording are noted in the docstrings.

## Building

    cd lean && lake build

Mathlib takes about 8 GB when built. On Daniel's Mac the folder
`.lake/packages` is a symlink to `~/github/sr-project/lean/.lake/packages`,
so both projects share one Mathlib (same toolchain and manifest).
On another machine, run `lake exe cache get` first.

Files import only the Mathlib modules they need; `import Mathlib`
makes each build take about ten minutes on this machine.

## Coverage

See `COVERAGE.md`.
