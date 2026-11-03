#!/bin/bash
# Rebuild the chemistry-*.png skeletal
# formulas in biology-assets/ from
# molecules.tex. Needs pdflatex and gs.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
out="$here/../../biology-assets"
work="$(mktemp -d)"
cp "$here/molecules.tex" "$work/"
cd "$work"
pdflatex -interaction=nonstopmode molecules >/dev/null
pdflatex -interaction=nonstopmode molecules >/dev/null
names=(pentane nonane isooctane rings alkenes
  suffixes priority natural giraffe insect)
for i in "${!names[@]}"; do
  gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m \
    -r300 -dTextAlphaBits=4 \
    -dGraphicsAlphaBits=4 \
    -dFirstPage=$((i + 1)) -dLastPage=$((i + 1)) \
    -sOutputFile="$out/chemistry-${names[$i]}.png" \
    molecules.pdf
done
rm -rf "$work"
